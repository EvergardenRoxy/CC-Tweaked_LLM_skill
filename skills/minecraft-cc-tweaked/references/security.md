# 安全：威胁模型、认证终端与常见误区

> 先想清楚"防谁、对方能做什么"，再选机制。CC 里很多"安全措施"只能挡住某一类人，用在错误的威胁上等于没有。本文件的代码均可运行（SHA-256 实现已对照标准测试向量验证）。

## 目录

- 一、威胁模型：防谁？
- 二、每层机制能挡住什么、挡不住什么
- 三、常见误区（网上教程里经常出现）
- 四、密码存储：加盐 + 迭代哈希（附纯 Lua SHA-256）
- 五、本地登录终端骨架
- 六、远程认证：挑战-应答与会话
- 七、检查清单

---

## 一、威胁模型：防谁？

| 级别 | 对手能做什么 | 现实例子 |
|---|---|---|
| A 网络旁观者 | 在无线范围内（或末影调制解调器任何地方）监听所有 rednet/modem 消息；伪造消息与发送者 ID；重放旧消息 | 同服玩家架一台监听计算机 |
| B 能操作终端 | 打开你的计算机界面：按键、长按 Ctrl+T/Ctrl+R/Ctrl+S、在旁边放磁盘驱动器和软盘 | 能走到你的基地里的玩家 |
| C 能破坏/放置方块 | 挖走计算机（文件跟着物品走）、把计算机放进自己的磁盘驱动器读全部文件、剪断红石、换外设 | 没有领地保护的服务器 |
| D 服主/OP | 读写世界存档、`/computercraft view` 远程打开终端、改配置 | 管理员 |

**结论先行**：
- 对 D 没有任何防护手段。
- 对 C，任何存放在该计算机上的东西都不是秘密；只能靠领地保护等游戏机制，或把秘密放在 C 接触不到的另一台计算机上。
- 对 B，关键是**让对方永远拿不到 shell 提示符**。
- 对 A，靠消息认证（挑战-应答、一次性随机数、会话过期），不信任发送者 ID。

## 二、每层机制能挡住什么、挡不住什么

| 机制 | 挡住 | 挡不住 / 注意 |
|---|---|---|
| `os.pullEvent = os.pullEventRaw`，并忽略 `terminate` | B 的 Ctrl+T | Ctrl+R（重启）和 Ctrl+S（关机）由游戏处理，Lua **无法拦截**；所以重启后必须**重新进入锁定**，启动文件本身就是锁 |
| 启动文件永不返回 shell（出错也回到登录界面，或 `os.reboot()`） | B 退出程序拿到 shell | 启动文件的任何未捕获错误都会落回 shell——主流程要 `pcall` 包住 |
| `settings.set("shell.allow_disk_startup", false)` + `settings.save()` | B 放软盘让磁盘上的启动文件优先运行 | 设置文件本身在计算机上，C 能改 |
| 不在终端保存明文密码、主密钥 | C 拆机读文件后直接拿到密码 | 拿到"密码哈希"仍可离线暴力破解，所以要加盐 + 迭代，并要求强密码 |
| 敏感数据放在另一台受保护的服务器，终端只做输入输出 | C 拆终端 | 服务器本身要在 C 接触不到的地方 |
| 挑战-应答 + 一次性随机数 + 过期时间 | A 抓包重放 | 验证值（verifier）泄露就等于密码泄露，验证值只存服务器 |
| 不信任 `rednet` 发送者 ID / 消息里的"用户名" | A 伪造身份 | 权限判断必须在服务器端，根据会话而不是客户端自称 |
| 失败计数 + 锁定时间写入文件 | B/A 暴力尝试 | 用 `os.epoch("utc")` 计时（重启不清零） |
| 审计日志 | 事后追查 | 日志不写密码；C 能删日志，重要日志发到服务器 |

## 三、常见误区（网上教程里经常出现）

| 误区 | 实际情况 |
|---|---|
| 调用 `textutils.sha256(...)` | **CC: Tweaked 没有内置任何哈希/加密函数**。需要自带纯 Lua 实现（见第四节），并验证它的输出 |
| `_G.shell = nil` 就能"禁用 shell" | `shell` 不在 `_G` 里，而是由 shell 注入到每个程序自己的环境中；这行代码对正在运行的 shell 没有作用 |
| 用 `os.run({}, "/system/kernel.lua")` 启动内核，再在内核里 `shell.run(...)` | `os.run` 不提供 `shell` API，内核里的 `shell` 是 nil，程序直接报错——然后**落回 shell**，锁失效 |
| 把 `fs.delete`、`os.reboot` 等设为 nil 就是沙箱 | 已经持有原函数引用的代码不受影响；能运行任意代码的人可以绕过。真正的边界是"不让对方运行代码"，而不是删 API |
| `tostring(math.random())` 作为会话令牌或随机数 | `math.random` 不是密码学随机数，可被预测。至少混入只有服务器知道的密钥再哈希（见第六节） |
| 服务器存 `SHA256(password .. salt)`，客户端发 `SHA256(password .. nonce)` | 两边算的不是同一个东西，服务器无法验证；正确做法见第六节 |
| "加密"函数里直接 `textutils.serialise` | 序列化不是加密。没有可靠加密库时，宁可**不在本机存敏感数据**，也不要假装加密 |
| 只靠 `os.pullEventRaw` 就认为"防住了" | 那只挡住 Ctrl+T；还要考虑重启、磁盘启动、拆机 |

## 四、密码存储：加盐 + 迭代哈希

- 每个用户一个随机盐；存 `verifier = H^N(盐 .. 密码)`（迭代 N 次增加暴力破解成本，N 取几百到几千，计算时要让出）。
- 比较时比较验证值，不比较密码。

```lua
-- sha256.lua：纯 Lua 5.2（bit32）实现，返回 64 位十六进制字符串
local band, bor, bxor, bnot = bit32.band, bit32.bor, bit32.bxor, bit32.bnot
local rrotate, rshift = bit32.rrotate, bit32.rshift

local K = {
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
}

local function preprocess(msg)
    local len = #msg
    local extra = 64 - ((len + 9) % 64)
    if extra == 64 then extra = 0 end
    local bits = len * 8
    local tail = {}
    for i = 7, 0, -1 do
        tail[#tail + 1] = string.char(math.floor(bits / 2 ^ (8 * i)) % 256)
    end
    return msg .. "\128" .. string.rep("\0", extra) .. table.concat(tail)
end

local function digest_block(msg, i, H)
    local w = {}
    for j = 1, 16 do
        local a, b, c, d = msg:byte(i + (j - 1) * 4, i + (j - 1) * 4 + 3)
        w[j] = ((a * 256 + b) * 256 + c) * 256 + d
    end
    for j = 17, 64 do
        local v15, v2 = w[j - 15], w[j - 2]
        local s0 = bxor(rrotate(v15, 7), rrotate(v15, 18), rshift(v15, 3))
        local s1 = bxor(rrotate(v2, 17), rrotate(v2, 19), rshift(v2, 10))
        w[j] = band(w[j - 16] + s0 + w[j - 7] + s1, 0xffffffff)
    end
    local a, b, c, d, e, f, g, h = H[1], H[2], H[3], H[4], H[5], H[6], H[7], H[8]
    for j = 1, 64 do
        local S1 = bxor(rrotate(e, 6), rrotate(e, 11), rrotate(e, 25))
        local ch = bxor(band(e, f), band(bnot(e), g))
        local t1 = h + S1 + ch + K[j] + w[j]
        local S0 = bxor(rrotate(a, 2), rrotate(a, 13), rrotate(a, 22))
        local maj = bxor(band(a, b), band(a, c), band(b, c))
        local t2 = S0 + maj
        h, g, f, e, d, c, b, a = g, f, e, band(d + t1, 0xffffffff), c, b, a, band(t1 + t2, 0xffffffff)
    end
    H[1] = band(H[1] + a, 0xffffffff); H[2] = band(H[2] + b, 0xffffffff)
    H[3] = band(H[3] + c, 0xffffffff); H[4] = band(H[4] + d, 0xffffffff)
    H[5] = band(H[5] + e, 0xffffffff); H[6] = band(H[6] + f, 0xffffffff)
    H[7] = band(H[7] + g, 0xffffffff); H[8] = band(H[8] + h, 0xffffffff)
end

local function sha256(msg)
    msg = preprocess(msg)
    local H = { 0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19 }
    for i = 1, #msg, 64 do
        digest_block(msg, i, H)
        if i % 4096 == 1 and os.queueEvent then      -- 长输入时定期让出
            os.queueEvent("sha256_yield")
            os.pullEvent("sha256_yield")
        end
    end
    return ("%08x%08x%08x%08x%08x%08x%08x%08x"):format(H[1], H[2], H[3], H[4], H[5], H[6], H[7], H[8])
end

return sha256
```

把上面保存为 `/lib/sha256.lua`，然后：

```lua
local sha256 = require("lib.sha256")

local ITERATIONS = 500

local function make_salt()
    local parts = {}
    for i = 1, 4 do parts[i] = ("%08x"):format(math.random(0, 0x7fffffff)) end
    return sha256(table.concat(parts) .. os.epoch("utc") .. os.getComputerID()):sub(1, 16)
end

local function derive(password, salt)
    local h = salt .. ":" .. password
    for i = 1, ITERATIONS do
        h = sha256(h .. salt)
        if i % 50 == 0 then os.queueEvent("kdf_yield") os.pullEvent("kdf_yield") end
    end
    return h
end

local salt = make_salt()
local verifier = derive("correct horse", salt)
print("stored:", salt, verifier)
print("check ok:", derive("correct horse", salt) == verifier)
print("check bad:", derive("wrong", salt) == verifier)
```

## 五、本地登录终端骨架

单机终端的目标：对 B 来说，**除了输入正确密码，没有任何途径拿到 shell**。

```lua
-- startup.lua（需要 /lib/sha256.lua 与 /data/users.db）
-- users.db 内容示例：{ admin = { salt = "...", verifier = "...", role = "admin" } }
local sha256 = require("lib.sha256")
local ITERATIONS = 500
local LOCK_FILE = "/data/lock.db"
local LOG_FILE = "/data/auth.log"
local LOCK_STEPS = { [3] = 30, [5] = 300, [8] = 1800 }   -- 失败次数 → 锁定秒数

local original_pull = os.pullEvent
os.pullEvent = os.pullEventRaw                           -- 忽略 Ctrl+T
settings.set("shell.allow_disk_startup", false)          -- 不允许软盘抢先启动
settings.save()

local function read_table(path, default)
    if not fs.exists(path) then return default end
    local h = fs.open(path, "r")
    local data = h and textutils.unserialise(h.readAll())
    if h then h.close() end
    return type(data) == "table" and data or default
end

local function write_table(path, data)
    local h = fs.open(path, "w")
    if h then h.write(textutils.serialise(data)) h.close() end
end

local function log(text)
    local h = fs.open(LOG_FILE, "a")
    if h then h.writeLine(os.date("!%Y-%m-%d %H:%M:%S") .. " " .. text) h.close() end
end

local function derive(password, salt)
    local h = salt .. ":" .. password
    for i = 1, ITERATIONS do
        h = sha256(h .. salt)
        if i % 50 == 0 then os.queueEvent("kdf_yield") os.pullEvent("kdf_yield") end
    end
    return h
end

local function locked_for()
    local lock = read_table(LOCK_FILE, { fails = 0, until_ms = 0 })
    return math.max(0, lock.until_ms - os.epoch("utc")) / 1000, lock
end

local function record(success, user)
    local _, lock = locked_for()
    if success then
        lock = { fails = 0, until_ms = 0 }
    else
        lock.fails = lock.fails + 1
        local seconds = 0
        for fails, secs in pairs(LOCK_STEPS) do
            if lock.fails >= fails and secs > seconds then seconds = secs end
        end
        lock.until_ms = os.epoch("utc") + seconds * 1000
    end
    write_table(LOCK_FILE, lock)
    log(("%s user=%s"):format(success and "LOGIN_OK" or "LOGIN_FAIL", tostring(user)))
end

local function login()
    term.setBackgroundColour(colours.black)
    term.clear()
    term.setCursorPos(1, 1)
    local wait = locked_for()
    if wait > 0 then
        print(("Locked. Try again in %d s"):format(math.ceil(wait)))
        sleep(math.min(wait, 5))
        return nil
    end
    write("User: ")
    local user = read()
    write("Password: ")
    local password = read("*")
    local users = read_table("/data/users.db", {})
    local entry = users[user]
    -- 用户不存在时也计算一次，避免通过响应时间判断用户名是否存在
    local ok = derive(password, entry and entry.salt or "x") == (entry and entry.verifier or "")
    record(ok, user)
    if ok then return user, entry.role end
    print("Access denied")
    sleep(2)
    return nil
end

local function session(user, role)
    print("Welcome, " .. user .. " (" .. tostring(role) .. ")")
    print("Type 'exit' to lock.")
    os.pullEvent = original_pull          -- 登录后恢复 Ctrl+T，方便用户停止自己的程序
    shell.run("shell")                    -- 已认证用户可以使用 shell；也可以换成受控菜单
    os.pullEvent = os.pullEventRaw        -- 退出 shell 后重新锁定
end

while true do
    local ok, err = pcall(function()
        local user, role = login()
        if user then session(user, role) end
    end)
    if not ok then log("ERROR " .. tostring(err)) end
    -- 无论成功、失败还是出错，都回到登录界面，绝不 return
end
```

要点与局限：
- 主循环永不退出、所有错误被 `pcall` 捕获——这才是"拿不到 shell"的关键。
- 重启后 `startup.lua` 重新运行，锁定状态在文件里，不会被重启清零。
- 认证成功后进入受控界面还是真正的 shell，取决于需求；进入 shell 后用户能修改启动文件，这是设计选择而不是漏洞。
- 对 C 无效：拆走计算机就能读 `users.db`（只能拿到验证值，配合强密码和迭代可以拖慢破解）和其他所有文件。

## 六、远程认证：挑战-应答与会话

终端不存任何秘密，验证值只在服务器上。流程：

```text
客户端 → 服务器：{type="hello", user="admin"}
服务器 → 客户端：{type="challenge", salt=该用户的盐, nonce=一次性随机数}
客户端：v = derive(密码, salt)；proof = sha256(nonce .. ":" .. v)
客户端 → 服务器：{type="proof", user="admin", nonce=..., proof=...}
服务器：nonce 必须是自己刚发的、未用过、未过期；计算 sha256(nonce .. ":" .. 存储的v) 比对
服务器 → 客户端：{type="session", token=..., expires=...}
之后的命令都带 token；服务器按 token 查用户和权限，过期即失效
```

- 服务器保存的 `v` 等同于密码（拿到 `v` 就能算出任何 proof），必须只放在服务器上。
- nonce 用完立即作废，并设短过期（如 30 秒），防止重放。
- 会话令牌：`sha256(服务器私有密钥 .. os.epoch("utc") .. 计数器 .. math.random())`，外人不知道私有密钥就无法预测；令牌有过期时间，可绑定客户端计算机 ID 作为额外校验（ID 可伪造，不能单独依赖）。
- 权限在服务器端按会话判断；客户端发来的"我是管理员"一律不信。
- 失败次数按用户和按来源分别限速。

服务器端骨架：

```lua
-- auth_server.lua（需要 /lib/sha256.lua；用户库只放在这台计算机上）
local sha256 = require("lib.sha256")
local PROTOCOL = "auth_v1"
local SERVER_KEY = sha256(tostring(math.random()) .. os.epoch("utc") .. os.getComputerID())
local USERS = { admin = { salt = "0123456789abcdef", verifier = "replace-with-derived-value", role = "admin" } }

local nonces, sessions, counter = {}, {}, 0

local function random_hex()
    counter = counter + 1
    return sha256(SERVER_KEY .. os.epoch("utc") .. counter .. math.random())
end

local function handle(sender, msg)
    if type(msg) ~= "table" then return nil end
    local now = os.epoch("utc")
    if msg.type == "hello" and USERS[msg.user] then
        local nonce = random_hex()
        nonces[nonce] = { user = msg.user, expires = now + 30000 }
        return { type = "challenge", salt = USERS[msg.user].salt, nonce = nonce }
    elseif msg.type == "proof" then
        local pending = type(msg.nonce) == "string" and nonces[msg.nonce]
        if not pending then return { type = "denied" } end
        nonces[msg.nonce] = nil                                   -- 一次性
        local user = USERS[pending.user]
        local expected = sha256(msg.nonce .. ":" .. user.verifier)
        if pending.expires < now or msg.proof ~= expected then return { type = "denied" } end
        local token = random_hex()
        sessions[token] = { user = pending.user, role = user.role, expires = now + 3600000, computer = sender }
        return { type = "session", token = token, expires = now + 3600000 }
    elseif msg.type == "command" then
        local s = type(msg.token) == "string" and sessions[msg.token]
        if not s or s.expires < now or s.computer ~= sender then return { type = "denied" } end
        if msg.action == "open_vault" and s.role ~= "admin" then return { type = "denied" } end
        return { type = "ok", action = msg.action }
    end
    return nil
end

peripheral.find("modem", rednet.open)
print("auth server ready")
while true do
    local sender, msg = rednet.receive(PROTOCOL)
    local ok, reply = pcall(handle, sender, msg)
    if ok and reply then rednet.send(sender, reply, PROTOCOL) end
end
```

（未知用户的 `hello` 不回复；需要隐藏"用户是否存在"时，可以对未知用户返回一个由用户名派生的假盐。）

## 七、检查清单

- [ ] 写出了威胁模型：防哪一级（A/B/C/D），以及明确**不防**什么。
- [ ] 没有使用不存在的 API（`textutils.sha256` 等）；哈希实现经过测试向量验证。
- [ ] 启动文件永不返回 shell，错误被捕获；Ctrl+T 被忽略；禁止磁盘启动。
- [ ] 不存明文密码；加盐、迭代；验证值只在需要的地方。
- [ ] 网络认证有一次性 nonce、过期时间、会话令牌；不信任发送者 ID 与客户端自称的身份。
- [ ] 失败锁定写文件、按真实时间计算；日志不含密码。
- [ ] 对用户说明局限：拆机、OP、物理接触无法用代码防住。
