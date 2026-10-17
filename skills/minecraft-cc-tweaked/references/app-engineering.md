# 大型程序工程化：结构、网络、安装更新、设置与可靠性

> 适用于几百行以上、长期运行、多人使用的程序（音乐播放器、仓储系统、基地控制台、带界面的应用）。**只在用户的目标确实需要、并且用户同意这种规模时才采用**；大多数需求先用简单脚本解决，以后再按本文件逐步加固。本文件的代码均为完整可运行的示例。

## 目录

- 项目结构与模块
- 可靠的异步 HTTP（请求标记、超时看门狗、重试策略、分块读取、Range 分段下载）
- 安装器与更新器（清单 → 全部下载 → 校验 → 写入）
- 设置持久化（默认值、校验、损坏回退）
- 外设选择、热插拔与功能探测
- 日志与错误呈现
- 界面：调色板、中文显示、后台任务（细节见 `ui-design.md`、`chinese-text.md`）
- 内存与性能
- 发布与持续集成

---

## 项目结构与模块

```text
/startup.lua            入口：只做装配（读取设置 → 创建模块 → 启动事件循环）
/app/net.lua            网络层（本文件的 HTTP 客户端）
/app/settings.lua       设置读写
/app/ui.lua             界面
/lib/...                第三方库（版本固定，单独存放）
/data/...               运行时数据（设置、缓存、日志）；与程序文件分开，更新时不覆盖
```

- 模块文件 `return` 一个表；入口用 `require("app.net")`（点号分隔，相对入口程序所在目录）。
- **全部用 `local`**。全局变量会在多个模块间互相覆盖，而且难以排查。需要共享的状态放进一个显式传递的表。
- **一个函数（包括文件的主代码块）最多 200 个 `local`**，第 201 个在编译时报 `main function has more than 200 local variables`。大文件里每个函数、每个常量都写成顶层 `local` 时会撞上这个上限。办法是**按功能把函数放进模块表**（`local M = {}`，`function M.draw() … end`，一张表里放几百个函数没有问题），并拆成多个文件用 `require`，而不是改成全局变量：全局变量更慢、会被别的代码覆盖，玩家打开 `bios.strict_globals` 设置后给全局变量赋值会直接报错（`Attempt to create global …`）。
- 程序文件和数据文件分目录：更新程序时整体替换程序目录，不碰 `/data`。
- 依赖的第三方库要固定版本（下载固定提交或发布版的地址），不要每次启动从"最新"地址动态加载。

## 可靠的异步 HTTP

`http.get` 是同步的，简单场景够用。长期运行、带界面、或多个任务同时联网时，要注意：

1. `http_success`/`http_failure` 事件只带 **URL** 区分请求。两个协程同时请求同一 URL（例如 `parallel` 里两个 `http.get`）会拿到同一个响应、另一个永远等不到。**解决：给每次请求的 URL 附加唯一标记参数**，用标记把事件分发回对应请求（如果服务器对未知查询参数敏感，例如签名 URL，就改为同一 URL 同时只发一个请求）。
2. 个别网络故障下可能迟迟不出现失败事件：**每个请求配一个计时器作看门狗**，超时按失败处理。
3. **按原因决定是否重试**：连接失败、超时、HTTP 408/429/5xx 可以重试（加退避）；其他 4xx 是参数或地址错误，重试无意义，直接报错。
4. **大响应分块读取并让出**：`readAll()` 读几 MB 数据可能触发 `Too long without yielding` 并卡住界面；用 `read(64 * 1024)` 循环，块之间让出。
5. 音频等二进制数据必须 `binary = true`。
6. 服务器默认单次下载上限约 16 MiB（`max_download`）。更大的文件用 `Range` 请求分段下载（服务器需支持，返回 206）。
7. 响应句柄用完一定 `close()`；无人认领的响应也要关闭。

```lua
-- net.lua：带请求标记、看门狗、重试与分块读取的 HTTP 客户端（在 parallel 的协程里使用）
local net = {}
local serial = 0
local RETRY_CODES = { [408] = true, [429] = true }

local function tag_url(url)
    serial = serial + 1
    local token = ("%d_%d"):format(os.epoch("utc"), serial)
    return url .. (url:find("?", 1, true) and "&" or "?") .. "_req=" .. token
end

local function yield_now()
    os.queueEvent("net_yield")
    os.pullEvent("net_yield")
end

local function read_body(res)
    local parts = {}
    while true do
        local chunk = res.read(64 * 1024)
        if chunk == nil or chunk == "" then break end
        parts[#parts + 1] = chunk
        yield_now()
    end
    return table.concat(parts)
end

local function header(headers, name)
    name = name:lower()
    for k, v in pairs(headers or {}) do
        if tostring(k):lower() == name then return v end
    end
end

-- 发一次请求；返回 body, code, headers 或 nil, 错误, 是否值得重试
local function attempt(opts)
    local url = tag_url(opts.url)
    local ok, accepted, reason = pcall(http.request, {
        url = url, method = opts.method, headers = opts.headers, body = opts.body,
        binary = opts.binary, timeout = opts.timeout,
    })
    if not ok then return nil, tostring(accepted), false end
    if accepted == false then return nil, tostring(reason or "request rejected"), false end

    local watchdog = os.startTimer(opts.timeout + 5)
    while true do
        local event, p1, p2, p3 = os.pullEvent()
        if event == "http_success" and p1 == url then
            os.cancelTimer(watchdog)
            local code = p2.getResponseCode()
            local headers = p2.getResponseHeaders()
            local body = read_body(p2)
            p2.close()
            if code >= 200 and code < 300 then return body, code, headers end
            return nil, "HTTP " .. code, RETRY_CODES[code] or code >= 500
        elseif event == "http_failure" and p1 == url then
            os.cancelTimer(watchdog)
            if p3 then
                -- 服务器返回了错误状态；读取后关闭
                local code = p3.getResponseCode()
                p3.close()
                return nil, "HTTP " .. code, RETRY_CODES[code] or code >= 500
            end
            return nil, tostring(p2), true
        elseif event == "timer" and p1 == watchdog then
            return nil, "timed out", true
        end
    end
end

-- opts: url, method, headers, body, binary, timeout(秒), retries
function net.request(opts)
    opts.timeout = opts.timeout or 15
    local retries = opts.retries or 3
    local err
    for i = 0, retries do
        local body, code_or_err, extra = attempt(opts)
        if body then return body, code_or_err, extra end
        err = code_or_err
        if not extra then break end           -- 不可重试的错误
        if i < retries then sleep(2 ^ i) end  -- 1, 2, 4 秒退避
    end
    return nil, err
end

-- 大文件：先探测总长度，再按块 Range 下载
function net.download_large(url, chunk_size)
    chunk_size = chunk_size or 8 * 1024 * 1024
    local probe, code, headers = net.request { url = url, headers = { Range = "bytes=0-0" }, binary = true }
    if not probe then return nil, code end
    local range = header(headers, "Content-Range")
    local total = range and tonumber(range:match("/(%d+)$"))
    if code ~= 206 or not total then
        return net.request { url = url, binary = true }   -- 服务器不支持 Range
    end
    local parts, start = {}, 0
    while start < total do
        local finish = math.min(total - 1, start + chunk_size - 1)
        local part, err = net.request {
            url = url, binary = true,
            headers = { Range = ("bytes=%d-%d"):format(start, finish) },
        }
        if not part then return nil, err end
        parts[#parts + 1] = part
        start = finish + 1
    end
    return table.concat(parts)
end

return net
```

使用：

```lua
local net = require("net")
local body, err = net.request { url = "https://example.com/api/status", timeout = 10, retries = 2 }
if not body then
    printError("Request failed: " .. tostring(err))
else
    local data = textutils.unserialiseJSON(body)
    print(data and "ok" or "not json")
end
```

- 在 `parallel` 的多个协程里同时调用 `net.request` 是安全的：每个请求的 URL 都不同，各协程只认领自己的事件。
- 等待响应期间，当前协程收到的其他事件（按键、rednet……）会被丢弃——所以把联网放在独立的协程里，由另一个协程处理用户输入。
- 如果程序有统一的事件循环（UI 框架），也可以改成回调式：发请求时把 `标记 → 回调` 存进表，在 `http_success`/`http_failure` 处理里解析标记并分发，再用计时器表实现看门狗。原理相同。

## 安装器与更新器

可靠的安装/更新流程：

1. 下载**清单**（要安装的文件列表 + 版本号）。
2. **把所有文件下载到内存**，任何一个失败就整体放弃——不会留下"新旧混杂"的半成品。
3. 校验：HTTP 状态 2xx、内容非空、`.lua` 文件能 `load` 编译通过。
4. 检查空间：需要的字节数 ≤ `fs.getFreeSpace` + 将被覆盖的旧文件大小。
5. 写入文件（先建目录），记录新版本号，提示重启。

```lua
-- installer.lua：用法 installer <清单网址>
-- 清单是一个返回表的 Lua 文件：
-- return { version = "1.2.0", base = "https://example.com/myapp/", files = { "startup.lua", "app/net.lua" } }
local manifest_url = ... or error("Usage: installer <manifest-url>", 0)

local function get(url)
    for i = 1, 3 do
        local res, err = http.get { url = url, binary = true, timeout = 15 }
        if res then
            local code = res.getResponseCode()
            local body = res.readAll()
            res.close()
            if code >= 200 and code < 300 and body and #body > 0 then return body end
            err = "HTTP " .. code
        end
        printError(("Download failed %s (%s), retry %d/3"):format(url, tostring(err), i))
        sleep(i)
    end
    error("Cannot download " .. url, 0)
end

local source = get(manifest_url)
local chunk, load_err = load(source, "=manifest", "t", {})
if not chunk then error("Cannot parse manifest: " .. load_err, 0) end
local manifest = chunk()
if type(manifest) ~= "table" or type(manifest.files) ~= "table" then error("Invalid manifest format", 0) end

-- 1. 全部下载到内存并校验
local downloads, needed, replaced = {}, 0, 0
for i, path in ipairs(manifest.files) do
    print(("[%d/%d] %s"):format(i, #manifest.files, path))
    local body = get(manifest.base .. path)
    if path:match("%.lua$") then
        local ok, err = load(body, "=" .. path)
        if not ok then error(path .. " failed to compile: " .. err, 0) end
    end
    downloads[#downloads + 1] = { path = "/" .. path, body = body }
    needed = needed + #body
    if fs.exists("/" .. path) and not fs.isDir("/" .. path) then
        replaced = replaced + fs.getSize("/" .. path)
    end
end

-- 2. 检查空间
local free = fs.getFreeSpace("/")
if free ~= "unlimited" and free + replaced < needed then
    error(("Not enough space: need %d bytes, have %d bytes"):format(needed, free + replaced), 0)
end

-- 3. 写入
for _, item in ipairs(downloads) do
    local dir = fs.getDir(item.path)
    if dir ~= "" and not fs.exists(dir) then fs.makeDir(dir) end
    local h = assert(fs.open(item.path, "wb"))
    h.write(item.body)
    h.close()
end

local h = fs.open("/.version", "w")
h.write(tostring(manifest.version or "?"))
h.close()
print("Installed version " .. tostring(manifest.version) .. ". Press any key to reboot")
os.pullEvent("key")
os.reboot()
```

- 用 `wget run <installer 地址>` 一行命令分发；清单放在固定的发布地址。
- 更新检查：启动时读本地 `/.version`，请求远端清单比较版本，有新版本时提示用户而不是静默覆盖。
- 清单用 `load(source, name, "t", {})` 在**空环境**里执行，避免远端文件随意改动全局环境。远端代码依然是可执行代码，只从自己信任的地址下载。
- 写文件时是逐个写入的；真正需要"原子"更新时，可先写到 `/app.new/` 目录，全部成功后 `fs.delete("/app")` 再 `fs.move("/app.new", "/app")`。

## 设置持久化

```lua
-- settings_store.lua：默认值 + 校验 + 损坏回退，不因为坏文件崩溃
local PATH = "/data/config.json"
local DEFAULTS = { monitor = nil, volume = 1, refresh = 5, speakers = {} }

local function clamp(x, lo, hi, default)
    x = tonumber(x)
    if not x then return default end
    return math.max(lo, math.min(hi, x))
end

local function normalize(raw)
    raw = type(raw) == "table" and raw or {}
    local cfg = {}
    cfg.monitor = type(raw.monitor) == "string" and raw.monitor ~= "" and raw.monitor or nil
    cfg.volume = clamp(raw.volume, 0, 3, DEFAULTS.volume)
    cfg.refresh = math.floor(clamp(raw.refresh, 1, 3600, DEFAULTS.refresh))
    cfg.speakers = {}
    local seen = {}
    for _, name in ipairs(type(raw.speakers) == "table" and raw.speakers or {}) do
        if type(name) == "string" and not seen[name] then
            seen[name] = true
            cfg.speakers[#cfg.speakers + 1] = name
        end
    end
    return cfg
end

local function load_config()
    if not fs.exists(PATH) then return normalize(nil), nil end
    local h = fs.open(PATH, "r")
    if not h then return normalize(nil), "Cannot open config file" end
    local text = h.readAll()
    h.close()
    local raw, err = textutils.unserialiseJSON(text)
    if raw == nil then return normalize(nil), "Config file corrupt, using defaults: " .. tostring(err) end
    return normalize(raw), nil
end

local function save_config(cfg)
    local text = textutils.serialiseJSON(normalize(cfg))
    local free = fs.getFreeSpace("/")
    if free ~= "unlimited" and free < #text then return false, "Not enough disk space" end
    if not fs.exists("/data") then fs.makeDir("/data") end
    local h, err = fs.open(PATH, "w")
    if not h then return false, err end
    h.write(text)
    h.close()
    return true
end

local cfg, warning = load_config()
if warning then printError(warning) end
cfg.volume = cfg.volume + 0.5
print(save_config(cfg))
```

要点：读取时**逐字段校验类型和范围**（用户手改、旧版本格式、写一半断电都会产生坏数据）；坏文件不让程序崩溃，而是回退默认并提示；保存前检查空间。简单的键值也可以直接用内置 `settings` API（`settings.define` 带 `type` 会拒绝错误类型）。

## 外设选择、热插拔与功能探测

- **首次运行让用户选择**外设并保存名字：网络上有多个显示器/扬声器时，`peripheral.find` 返回的第一个不一定是用户想要的。保存的名字不存在了（被拆掉、编号变了）就重新进入选择流程。
- **热插拔**：监听 `peripheral`/`peripheral_detach` 更新外设列表；长期运行的程序调用外设方法时用 `pcall`，外设刚好被拆掉时不至于整个程序崩溃。

```lua
-- 维护在线扬声器列表，接入/断开时自动更新
local speakers = {}

local function rescan()
    speakers = {}
    for _, name in ipairs(peripheral.getNames()) do
        if peripheral.hasType(name, "speaker") then
            speakers[name] = peripheral.wrap(name)
        end
    end
end

local function chime()
    for name, sp in pairs(speakers) do
        local ok = pcall(sp.playNote, "bell", 1, 12)
        if not ok then speakers[name] = nil end   -- 调用时已断开
    end
end

rescan()
while true do
    local event, name = os.pullEvent()
    if event == "peripheral" or event == "peripheral_detach" then
        rescan()
        print(event, name)
    elseif event == "key" then
        chime()
    end
end
```

- **功能探测而不是版本比较**：可选的库或附属模组提供的扩展方法，用 `pcall(require, "模块名")` 或 `type(obj.method) == "function"` 判断，缺失时降级到标准实现。

```lua
local ok_lib, base64 = pcall(require, "cc.base64")      -- 1.119.0+ 才有
if not ok_lib then base64 = nil end
local speaker = peripheral.find("speaker")
local has_audio = speaker ~= nil and type(speaker.playAudio) == "function"   -- 1.100+
print("base64:", base64 ~= nil, "playAudio:", has_audio)
```

## 日志与错误呈现

- 写一个统一的日志函数：带级别和时间，写入 `/data/log.txt`，文件超过一定大小就轮换（重命名为 `.old`），避免占满磁盘。
- **日志脱敏**：URL 参数、请求体里的 cookie、token、密码写日志前替换为 `<redacted>`。
- **用户只看最终结果**：重试过程写日志，不弹窗；全部重试失败后才给用户一条可读的错误（"网络请求超时，请检查网络连接"）。
- 界面回调（按钮点击、事件处理）里的逻辑用 `pcall` 包住，单个操作失败只提示错误，不中断主循环。

```lua
local LOG = "/data/log.txt"
local MAX_LOG = 64 * 1024

local function redact(text)
    return (tostring(text)
        :gsub("([?&][Tt]oken=)[^&%s]+", "%1<redacted>")
        :gsub("([Cc]ookie[\"']?%s*[:=]%s*[\"']?)[^\"'&%s]+", "%1<redacted>"))
end

local function log(level, msg)
    if not fs.exists("/data") then fs.makeDir("/data") end
    if fs.exists(LOG) and fs.getSize(LOG) > MAX_LOG then
        if fs.exists(LOG .. ".old") then fs.delete(LOG .. ".old") end
        fs.move(LOG, LOG .. ".old")
    end
    local h = fs.open(LOG, "a")
    if h then
        h.writeLine(("%s [%s] %s"):format(os.date("!%Y-%m-%d %H:%M:%S"), level, redact(msg)))
        h.close()
    end
end

local function safely(action, ...)
    local ok, err = pcall(action, ...)
    if not ok then
        log("error", err)
        printError("Action failed: " .. tostring(err))
    end
    return ok
end

log("info", "request https://example.com/a?token=abc123&x=1")
safely(function() error("demo failure") end)
```

## 界面：调色板、中文显示、后台任务

- **调色板**（深色主题等）和界面布局：见 `ui-design.md`，退出时要恢复调色板。
- **中文显示**：CC 的终端和显示器不能显示中文；用户要中文界面时的选择（utf8display 点阵字体、Create 显示板、聊天框）和前提见 `chinese-text.md`。
- **后台任务**：高级计算机上 shell 程序 `bg <程序>` 在新标签页后台运行另一个程序（如键盘服务、网络监听），主程序继续前台运行；或者在同一程序内用 `parallel`。
- 复杂界面（按钮、列表、滚动、布局）可考虑成熟的第三方 UI 框架（如 Basalt），比手写事件分发省事；它们一般接管主事件循环，事件要通过框架提供的接口注册。

## 内存与性能

- 计算机内存不是无限的：大音频、大图片只**缓存少量**（例如最近 2 首），用表记录顺序，超出时删除最旧的。
- 大字符串反复 `..` 拼接很慢且占内存：先放进表，最后 `table.concat`。
- 需要大量外设调用时批量并发（`parallel.waitForAll`，分批），但别让单个循环长时间不让出。
- 定时刷新的界面只重绘变化的部分，或画到隐藏的 `window` 再一次显示。

## 发布与持续集成

- 在仓库里保存源代码，用 CI（如 GitHub Actions）在每次提交时对所有 `.lua` 文件运行 Lua 5.2 的 `luac -p` 做语法检查，防止把语法错误发布给用户。
- 发布目录与源码目录分开；用户的安装器只从发布目录下载。可以在 CI 中压缩代码减小体积，但压缩后要再跑一次 `luac -p`。
- 版本号放在单独的文件里，安装器和更新检查都读它。
