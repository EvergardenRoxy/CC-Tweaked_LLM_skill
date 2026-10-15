# API 参考（全局 API 与 `cc.*` 库）

> 来源：<https://tweaked.cc> 各模块页面。`[x]` 表示可选参数；"返回 `a, b`"按顺序给出多返回值。外设方法见 `peripherals.md`，海龟见 `turtle.md`，网络见 `networking.md`。
> 用户的 CC: Tweaked 版本较旧时，带"（版本）"标注的功能可能不存在。

## 目录

- 全局函数（`_G`）
- `os`、`fs`（含文件句柄）、`io`
- `term`、`window`、`colors`/`colours`、`paintutils`
- `textutils`、`settings`、`shell`、`multishell`、`help`、`keys`
- `redstone`/`rs`、`disk`、`parallel`、`vector`、`pocket`、`commands`
- `cc.*` 库（`require` 加载）

---

## 全局函数（`_G`，由 bios.lua 定义）

| 函数 | 说明 |
|---|---|
| `sleep([秒=0])` | 暂停；向上取整到 0.05 秒；**丢弃等待期间的其他事件** |
| `write(文本)` | 写到终端，自动折行，不换行；返回写了几行 |
| `print(...)` | 空格分隔打印并换行，自动折行；返回行数 |
| `printError(...)` | 红色打印 |
| `read([替换字符 [, 历史表 [, 补全函数 [, 默认值]]]])` | 读一行输入；`read("*")` 隐藏密码 |
| `_HOST` | 字符串，如 `ComputerCraft 1.93.0 (Minecraft 1.15.2)` |
| `_CC_DEFAULT_SETTINGS` | 配置文件里的默认设置字符串 |

标准 Lua 全局：`pairs ipairs next select type tostring tonumber pcall xpcall error assert rawget rawset rawequal rawlen setmetatable getmetatable load loadfile dofile require`；库 `string table math coroutine bit32 utf8 debug`。**没有** `collectgarbage`。

---

## `os`

| 函数 | 说明 |
|---|---|
| `os.pullEvent([过滤])` | 等事件，返回 `事件名, 参数…`；收到 `terminate` 时终止程序 |
| `os.pullEventRaw([过滤])` | 同上但会返回 `terminate`（即使设置了过滤也会返回它） |
| `os.queueEvent(名, ...)` | 往自己的队列塞事件（参数不能含函数） |
| `os.startTimer(秒)` → id | 到时产生 `timer, id`；向上取整到 0.05 秒 |
| `os.cancelTimer(id)` | 取消计时器 |
| `os.setAlarm(游戏时间0–24)` → id | 到游戏内时间产生 `alarm, id` |
| `os.cancelAlarm(id)` | 取消闹钟 |
| `os.sleep(秒)` | 同 `sleep` |
| `os.clock()` | 本计算机已运行秒数 |
| `os.time([locale])` | 默认 `"ingame"`：游戏内小时 0–24；`"utc"`/`"local"`：现实时间小时；传 `os.date("*t")` 表则返回 UNIX 时间戳 |
| `os.day([locale])` | 天数 |
| `os.epoch([locale])` | 毫秒；`os.epoch("utc")` 是现实 UNIX 毫秒；`"ingame"` 下 1 现实秒 = 72000 |
| `os.date([格式 [, 时间]])` | strftime 格式；`"*t"`/`"!*t"` 返回表；`!` 前缀用 UTC |
| `os.getComputerID()` / `os.computerID()` | 计算机 ID |
| `os.getComputerLabel()` / `os.computerLabel()` / `os.setComputerLabel([名])` | 标签 |
| `os.version()` | `"CraftOS 1.9"` |
| `os.run(env, 路径, ...)` | 用指定环境运行程序（不解析程序名、不提供 `shell`） |
| `os.reboot()` / `os.shutdown()` | 重启 / 关机 |
| `os.loadAPI(路径)` / `os.unloadAPI(名)` | **已弃用**，改用 `require` |

没有：`os.execute os.exit os.getenv os.remove os.rename os.tmpname os.difftime`。

---

## `fs`

所有路径都是**绝对路径**（不考虑 shell 当前目录；需要时用 `shell.resolve`）。

| 函数 | 说明 |
|---|---|
| `fs.open(路径, 模式)` | 模式 `"r" "w" "a"`，1.109.0+ 还有 `"r+" "w+"`；末尾加 `b` 为二进制。返回句柄，或 `nil, 原因` |
| `fs.exists(p)` / `fs.isDir(p)` / `fs.isReadOnly(p)` | 布尔 |
| `fs.list(p)` | 目录下的名字列表（字典序）；路径不存在则报错 |
| `fs.find(通配)` | `*`、`?`（1.106.0+）匹配单段路径 |
| `fs.makeDir(p)` | 递归创建目录 |
| `fs.move(a, b)` / `fs.copy(a, b)` | 需要时自动建父目录；目标已存在会报错 |
| `fs.delete(p)` | 删除文件或整个目录 |
| `fs.combine(a, ...)` | 拼路径（1.95.0+ 支持多参数） |
| `fs.getName(p)` / `fs.getDir(p)` | 文件名 / 父目录 |
| `fs.getSize(p)` | 字节数 |
| `fs.getDrive(p)` | `"hdd"`、`"rom"` 或磁盘挂载名 |
| `fs.getFreeSpace(p)` / `fs.getCapacity(p)` | 剩余空间（可能是 `"unlimited"`）/ 容量（只读盘为 `nil`） |
| `fs.attributes(p)` | `{size, isDir, isReadOnly, created, modified}`（毫秒时间戳） |
| `fs.isDriveRoot(p)` | 是否是挂载点 |
| `fs.complete(...)` | 路径补全（配合 `read`） |

**文件句柄方法（用 `.` 调用）**

| 读句柄 | 写句柄 |
|---|---|
| `h.readLine([保留换行])` → 字符串或 `nil`（文件尾） | `h.write(字符串或字节)` |
| `h.readAll()` → 剩余内容 | `h.writeLine(文本)` |
| `h.read([字节数])` | `h.flush()` |
| `h.seek([whence [, offset]])` → 新位置 | `h.seek(...)` |
| `h.close()` | `h.close()` |

用完一定要 `close()`，否则写入可能丢失、文件被占用。1.109.0 起非二进制模式也读写原始字节（不再做 UTF-8 转换）。

```lua
local function read_file(path)
    local h, err = fs.open(path, "r")
    if not h then return nil, err end
    local text = h.readAll()
    h.close()
    return text
end

local function write_file(path, text)
    local h = assert(fs.open(path, "w"))
    h.write(text)
    h.close()
end

write_file("/log.txt", "start\n")
print(read_file("/log.txt"))
```

## `io`（模拟标准 Lua io）

`io.open(文件名 [, 模式])` 返回句柄或 `nil, 错误`；`io.lines([文件名, ...])`；`io.read(...)`、`io.write(...)`；`io.input([f])`、`io.output([f])`、`io.close([f])`、`io.flush()`、`io.type(obj)`；`io.stdin/stdout/stderr`。
**io 句柄用 `:` 调用**：`f:read("l")`、`f:read("a")`、`f:lines()`、`f:write(...)`、`f:seek(...)`、`f:close()`。`io.lines(文件, 16 * 1024)` 可按块读取（音频示例常用）。1.111.0+ 支持 `r+`、`w+`。

---

## `term`（也是所有"终端对象"的方法集合：显示器、窗口）

| 函数 | 说明 |
|---|---|
| `term.write(文本)` | 在光标处写，不换行不折行 |
| `term.blit(文本, 前景, 背景)` | 三个字符串等长，颜色用 `0-9a-f` |
| `term.clear()` / `term.clearLine()` | 用当前背景色清屏 / 清当前行 |
| `term.getCursorPos()` → x, y / `term.setCursorPos(x, y)` | 坐标从 1 开始 |
| `term.getCursorBlink()` / `term.setCursorBlink(bool)` | 光标闪烁 |
| `term.getSize()` → 宽, 高 | 计算机 51×19，口袋 26×20，海龟 39×13 |
| `term.scroll(n)` | 上移 n 行（负数下移） |
| `term.setTextColour(c)` / `setTextColor` / `getTextColour` | 文字颜色 |
| `term.setBackgroundColour(c)` / `setBackgroundColor` / `getBackgroundColour` | 背景颜色 |
| `term.isColour()` / `isColor()` | 是否支持颜色（普通计算机为 false，颜色显示为灰度） |
| `term.setPaletteColour(c, 0xRRGGBB)` 或 `(c, r, g, b)`（0–1） / `getPaletteColour(c)` | 调色板 |
| `term.nativePaletteColour(c)` | 默认调色板值 |
| `term.redirect(目标)` → 旧目标 | 之后 `print`/`write`/`term.*` 都画到目标上 |
| `term.current()` / `term.native()` | 当前 / 原生终端对象 |

终端尺寸以 `term.getSize()` 为准（上表为常见默认值，多标签 `multishell` 会占一行）。

## `window`

`window.create(父终端, x, y, 宽, 高 [, 可见=true])` 返回窗口对象（终端对象，可 `term.redirect`）。父终端不能是 `term` 本身，用 `term.current()`、`term.native()` 或显示器。
窗口额外方法：`setVisible(bool)`、`isVisible()`、`redraw()`、`restoreCursor()`、`getPosition()`、`reposition(x, y [, 宽, 高 [, 新父]])`、`getLine(y)` → 文本, 前景, 背景。
用途：双缓冲防闪烁——先 `win.setVisible(false)`，画完再 `win.setVisible(true)`。

## `colors` / `colours`

| 常量 | 值 | blit | 常量 | 值 | blit |
|---|---|---|---|---|---|
| `white` | 1 | `0` | `lightGray`/`lightGrey` | 256 | `8` |
| `orange` | 2 | `1` | `cyan` | 512 | `9` |
| `magenta` | 4 | `2` | `purple` | 1024 | `a` |
| `lightBlue` | 8 | `3` | `blue` | 2048 | `b` |
| `yellow` | 16 | `4` | `brown` | 4096 | `c` |
| `lime` | 32 | `5` | `green` | 8192 | `d` |
| `pink` | 64 | `6` | `red` | 16384 | `e` |
| `gray`/`grey` | 128 | `7` | `black` | 32768 | `f` |

（`grey`/`lightGrey` 只在 `colours` 里。）函数：`combine(...)`、`subtract(集合, ...)`、`test(集合, 颜色)`、`packRGB(r,g,b)`、`unpackRGB(rgb)`、`rgb8(...)`、`toBlit(颜色)`（1.94.0+）、`fromBlit(字符)`（1.105.0+）。

## `paintutils`

`parseImage(字符串)`、`loadImage(路径)`、`drawPixel(x, y [, 颜色])`、`drawLine(x1, y1, x2, y2 [, 颜色])`、`drawBox(...)`（空心）、`drawFilledBox(...)`、`drawImage(图像, x, y)`。绘制到当前终端（可先 `term.redirect` 到显示器）。

---

## `textutils`

| 函数 | 说明 |
|---|---|
| `serialise(t [, {compact, allow_repetitions}])` / `serialize` | Lua 值 → 字符串（不能含函数、递归表） |
| `unserialise(s)` / `unserialize` | 字符串 → Lua 值，失败返回 `nil` |
| `serialiseJSON(t [, 选项])` / `serializeJSON` | → JSON；选项 `nbt_style`、`unicode_strings`、`allow_repetitions` |
| `unserialiseJSON(s [, 选项])` / `unserializeJSON` | JSON → Lua，失败返回 `nil, 原因`；选项 `nbt_style`、`parse_null`、`parse_empty_array` |
| `json_null` / `empty_json_array` | 表示 JSON 的 `null` / 空数组 |
| `urlEncode(s)` | URL 编码 |
| `formatTime(时间 [, 24小时制])` | `os.time()` → `"6:30 PM"` |
| `slowWrite(文本 [, 速率])` / `slowPrint` | 逐字输出 |
| `pagedPrint(文本 [, 留空行])` / `tabulate(...)` / `pagedTabulate(...)` | 分页/表格打印 |
| `complete(文本 [, 环境])` | Lua 表达式补全 |

## `settings`

| 函数 | 说明 |
|---|---|
| `settings.define(名, {description, default, type})` | 声明设置；`type` 为 `"number" "string" "boolean" "table"`（1.87.0+） |
| `settings.get(名 [, 默认])` / `settings.set(名, 值)` / `settings.unset(名)` | 读 / 写 / 恢复默认 |
| `settings.save([路径=".settings"])` / `settings.load([路径])` | **`set` 不会自动保存** |
| `settings.getNames()` / `getDetails(名)` / `undefine(名)` / `clear()` | |

修改会触发 `setting_changed` 事件。系统设置例：`shell.allow_startup`、`shell.allow_disk_startup`、`motd.enable`、`lua.autocomplete`；shell 中用 `set 名 值` 修改。

## `shell`（只在由 shell 启动的程序中可用）

`shell.run(程序, 参数...)`（参数拼接后重新解析）、`shell.execute(程序, ...)`（不解析）、`shell.exit()`、`shell.dir()`/`setDir(d)`、`shell.path()`/`setPath(p)`、`shell.resolve(相对路径)`、`shell.resolveProgram(名)`、`shell.programs([含隐藏])`、`shell.getRunningProgram()`、`shell.setAlias(别名, 程序)`/`clearAlias`/`aliases()`、`shell.complete(行)`、`shell.setCompletionFunction(程序, 函数)`、`shell.openTab(...)`、`shell.switchTab(id)`（后两者需高级计算机的 multishell）。

## `multishell`（高级计算机）

`getFocus()`、`setFocus(n)`、`getTitle(n)`、`setTitle(n, 标题)`、`getCurrent()`、`launch(环境, 路径, ...)`、`getCount()`。

## `help`

`help.path()`、`setPath(p)`、`lookup(主题)`、`topics()`、`completeTopic(前缀)`。

## `keys`

键码常量：`keys.a … keys.z`、`keys.one … keys.zero`、`keys.enter`、`keys.space`、`keys.backspace`、`keys.tab`、`keys.up/down/left/right`、`keys.leftCtrl`、`keys.leftShift`、`keys.f1`… 键码数值随版本变化，**只用常量**。`keys.getName(code)` → 名字或 `nil`。

---

## `redstone` / `rs`

| 函数 | 说明 |
|---|---|
| `getSides()` | `{"top","bottom","left","right","front","back"}` |
| `setOutput(面, bool)` / `getOutput(面)` / `getInput(面)` | 数字信号（开 = 15） |
| `setAnalogOutput(面, 0–15)` / `getAnalogOutput(面)` / `getAnalogInput(面)` | 模拟信号；英式拼写 `Analogue` 版本同样存在 |
| `setBundledOutput(面, 颜色掩码)` / `getBundledOutput(面)` / `getBundledInput(面)` / `testBundledInput(面, 掩码)` | 捆绑线缆（需要 Project:Red 等模组） |

任一输入变化触发 `redstone` 事件（无参数，需要自己再读各面）。

## `disk`（参数是驱动器名/方向）

`isPresent(名)`、`hasData(名)`、`getMountPath(名)`、`getLabel(名)`、`setLabel(名, 标签)`、`getID(名)`、`hasAudio(名)`、`getAudioTitle(名)`、`playAudio(名)`、`stopAudio(名)`、`eject(名)`。驱动器外设方法见 `peripherals.md`。

## `parallel`

- `parallel.waitForAny(f1, f2, ...)`：任一函数结束即返回（返回结束的序号）；任一报错则向上抛。
- `parallel.waitForAll(f1, f2, ...)`：全部结束才返回；1.120.0+ 每个函数可接收 `spawn` 参数动态添加新任务。
- 注意：事件队列只有 256 个，HTTP 同时最多 16 个请求；不要一次并行几百个外设调用。

## `vector`

`vector.new(x, y, z)` 返回向量对象，**方法用 `:`**：`v:add(o)`、`v:sub(o)`、`v:mul(数)`、`v:div(数)`、`v:unm()`、`v:dot(o)`、`v:cross(o)`、`v:length()`、`v:normalize()`、`v:round([容差])`、`v:tostring()`、`v:equals(o)`；也支持运算符 `+ - * / ==` 与 `tostring(v)`。

## `pocket`（仅口袋计算机，可用 `if pocket then` 判断）

`pocket.equipBack()` → `ok, 原因`（从玩家背包换装升级）；`pocket.unequipBack()` → `ok, 原因`。

## `commands`（仅命令计算机）

| 函数 | 说明 |
|---|---|
| `commands.exec(命令)` | 返回 `成功, 输出行表, 影响数量` |
| `commands.execAsync(命令)` → 任务 id | 完成时触发 `task_complete` |
| `commands.<命令名>(参数...)` | 自动生成的辅助函数，如 `commands.say("Hi")`、`commands.setblock("~", "~1", "~", "minecraft:stone")`；`commands.async.<命令名>` 为异步版 |
| `commands.list(...)` | 可用命令 |
| `commands.getBlockPosition()` → x, y, z | 自身坐标 |
| `commands.getDimension()` | 维度名（1.119.0+） |
| `commands.getBlockInfo(x, y, z [, 维度])` / `getBlockInfos(x1,y1,z1,x2,y2,z2 [, 维度])` | 方块详情（字段见 `peripherals.md` 的"方块详情"） |
| `commands.getEntities(选择器)` | 实体详情（1.118.0+） |

---

## `cc.*` 库（用 `require` 加载）

| 模块 | 主要函数 |
|---|---|
| `cc.expect` | `expect(序号, 值, 类型...)`、`field(表, 键, 类型...)`、`range(数, [最小], [最大])`——参数校验 |
| `cc.strings` | `wrap(文本 [, 宽])`、`ensure_width(行 [, 宽])`、`split(字符串, 分隔符 [, plain [, limit]])`（1.112.0+） |
| `cc.pretty` | `pretty_print(值)`——比 `textutils.serialise` 更适合调试打印 |
| `cc.completion` | `choice`、`peripheral`、`side`、`setting`、`command`——给 `read` 用的补全 |
| `cc.shell.completion` | `build(...)`、`file`、`dir`、`program`……——给 `shell.setCompletionFunction` 用 |
| `cc.audio.dfpwm` | `make_decoder()`、`make_encoder()`、`decode(s)`、`encode(t)`（1.100.0+） |
| `cc.image.nft` | `parse(s)`、`load(路径)`、`draw(图像, x, y [, 终端])` |
| `cc.base64` | `encode(s [, alt])`、`decode(s [, alt])`（1.119.0+） |
| `cc.require` | `make(env, dir)`——自建 `require` |

```lua
local expect = require("cc.expect").expect
local strings = require("cc.strings")
local pretty = require("cc.pretty")

local function greet(name)
    expect(1, name, "string")
    return "Hello, " .. name
end

for _, line in ipairs(strings.wrap(greet("Steve") .. " and a long tail of text", 20)) do
    print(line)
end
pretty.pretty_print({ a = 1, b = { true, "x" } })
```
