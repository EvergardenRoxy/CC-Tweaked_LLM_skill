# 网络：rednet、modem、GPS、HTTP

> 来源：tweaked.cc 的 `rednet`、`modem`、`gps`、`http` 页面，"Setting up GPS"、"Allowing access to local IPs" 指南。

## 目录

- 调制解调器种类
- rednet（推荐）
- modem 原始通信
- GPS
- HTTP 与 WebSocket
- 安全提示

---

## 调制解调器种类

| 种类 | 范围 | 说明 |
|---|---|---|
| 无线调制解调器 | 64 格；y=96 以上范围线性增大，最高 384 | 可贴在计算机上，或作为海龟/口袋计算机升级 |
| 末影调制解调器 | 无限、跨维度 | 无线的升级版 |
| 有线调制解调器 + 网线 | 同一网线网络 | 还能连接远程外设（见 `peripherals.md`） |

- 信道 0–65535；每个调制解调器最多同时打开 128 个信道。
- rednet 占用：计算机 ID 对应信道、广播 65535（`rednet.CHANNEL_BROADCAST`）、中继 65533（`CHANNEL_REPEAT`）；GPS 用 65534（`gps.CHANNEL_GPS`）。ID ≥ 65500 时信道回绕。
- 消息载荷可以是数字、字符串、布尔、表；函数和元表不会被传输。

## rednet（推荐）

| 函数 | 说明 |
|---|---|
| `rednet.open(调制解调器名)` | 打开（同时监听本机 ID 信道和广播信道）；不存在报错 |
| `rednet.close([名])` / `rednet.isOpen([名])` | 关闭 / 是否打开 |
| `rednet.send(目标ID, 消息 [, 协议])` | 返回是否发出（不保证对方收到） |
| `rednet.broadcast(消息 [, 协议])` | 发给所有 rednet 计算机 |
| `rednet.receive([协议过滤 [, 超时秒]])` | 返回 `发送者ID, 消息, 协议`；超时返回 `nil` |
| `rednet.host(协议, 主机名)` | 注册服务；同网络同协议主机名不能重复，`localhost` 保留 |
| `rednet.unhost(协议)` | 取消注册 |
| `rednet.lookup(协议 [, 主机名 [, 超时=2]])` | 无主机名：返回所有主机 ID（多返回值）；有主机名：返回一个 ID 或 `nil`（超时参数 1.118.0+） |

- `rednet.run()` 在开机时自动在后台运行，**不要手动调用**。
- 收到消息时产生 `rednet_message, 发送者ID, 消息, 协议` 事件（之前还有一个 `modem_message`），可在自己的事件循环中处理。
- 打开所有调制解调器：`peripheral.find("modem", rednet.open)`。

**请求-响应示例**

```lua
-- 服务端：保存为 server.lua
peripheral.find("modem", rednet.open)
rednet.host("demo", "server1")
print("server id", os.getComputerID())
while true do
    local id, msg = rednet.receive("demo")
    if type(msg) == "table" and msg.cmd == "ping" then
        rednet.send(id, { ok = true, time = os.epoch("utc") }, "demo")
    end
end
```

```lua
-- 客户端
peripheral.find("modem", rednet.open)
local server = rednet.lookup("demo", "server1")
if not server then error("找不到 server1（服务端是否在运行、是否在范围内？）", 0) end
rednet.send(server, { cmd = "ping" }, "demo")
local id, reply = rednet.receive("demo", 5)
if id == server and reply then
    print("pong", reply.time)
else
    printError("超时")
end
```

注意：`rednet.receive` 会消耗等待期间的其他事件；同时要处理按键/计时器时，在事件循环里直接处理 `rednet_message` 事件，或用 `parallel`。

## modem 原始通信

| 方法 | 说明 |
|---|---|
| `modem.open(信道)` / `isOpen` / `close` / `closeAll()` | 接收前必须打开信道 |
| `modem.transmit(信道, 回复信道, 载荷)` | 发送不需要打开信道；对方回复要发到"回复信道"，本机需打开它才能收到 |
| `modem.isWireless()` | 是否无线 |

接收：事件 `modem_message, 调制解调器名, 信道, 回复信道, 消息, 距离`（跨维度时距离为 `nil`）。

```lua
local modem = peripheral.find("modem") or error("没有调制解调器", 0)
modem.open(43)
modem.transmit(15, 43, "Hello")
local event, side, channel, reply, message, distance
repeat
    event, side, channel, reply, message, distance = os.pullEvent("modem_message")
until channel == 43
print("reply:", tostring(message), "distance:", tostring(distance))
```

## GPS

**搭建星座**（官方指南）：
1. 4 台计算机 + 4 个末影调制解调器（普通无线范围很小）。
2. 选一个约 10×10×10 的区域，最好在常加载区块（出生点区块等）；三台放在底面三个相邻角落，第四台在第一台正上方顶部，每台**顶部**放调制解调器。4 台需在每个轴上都有差异，不能共面。
3. F3 查看每台计算机的坐标（看向方块时的 Targeted Block），在每台上 `edit startup.lua`：

```lua
-- 把 x, y, z 换成这台计算机自己的坐标
local x, y, z = 100, 70, 200
shell.run("gps", "host", x, y, z)
```

4. 重启每台计算机。测试：另一台带无线调制解调器的计算机运行 `gps locate`。

**定位**：`local x, y, z = gps.locate(2)`，失败返回 `nil`（星座不在范围、主机少于需要的数量、调制解调器未装）。`gps.locate(超时, true)` 打印调试信息。海龟需要装无线调制解调器升级。

## HTTP 与 WebSocket

| 函数 | 说明 |
|---|---|
| `http.get(url [, 头表 [, 二进制]])` 或 `http.get{url=, headers=, binary=, method=, redirect=, timeout=}` | 同步请求；返回响应句柄，或 `nil, 错误, 失败的响应?` |
| `http.post(url, 正文 [, 头表 [, 二进制]])` 或表形式 | 同上 |
| `http.request(...)` | 异步，结果为 `http_success, url, 句柄` / `http_failure, url, 错误, 句柄?` 事件 |
| `http.checkURL(url)` / `checkURLAsync(url)` | 是否允许访问（被屏蔽返回 `false, 原因`） |
| `http.websocket(url [, 头表])` 或表形式 | 返回 WebSocket，或 `false, 错误` |
| `http.websocketAsync(...)` | 异步，事件 `websocket_success` / `websocket_failure` |

响应句柄：与文件读句柄相同的方法（`readAll`、`readLine`、`read`、`close`），外加 `getResponseCode()` → `200, "OK"`、`getResponseHeaders()`。
WebSocket：`ws.send(消息 [, 二进制])`、`ws.receive([超时])` → `消息, 是否二进制` 或超时 `nil`、`ws.close()`；事件 `websocket_message`、`websocket_closed`。

```lua
local res, err = http.get("https://example.com/data.json")
if not res then error("请求失败: " .. tostring(err), 0) end
local body = res.readAll()
res.close()
local data = textutils.unserialiseJSON(body)
print(data and "parsed" or "not json")
```

- 同时最多 16 个 HTTP 请求（`parallel` 并发也不会更多）。
- 服务器可在 `computercraft-server.toml` 关闭 HTTP 或按域名设置规则；默认禁止访问局域网/本机地址（`$private` 规则），本地测试需要服务器主改配置（见 `config-and-versions.md`）。
- 1.109.0+ 响应以原始字节读取，不再做 UTF-8 解码。
- 下载程序：`wget <url> [文件名]`、`wget run <url>`、`pastebin get <代码> <文件名>`、`pastebin run <代码>`——都依赖 HTTP 已启用。

## 安全提示

- rednet/modem 消息可被任何人监听、伪造（ID 也可伪造）。多人服务器上：校验协议和发送者、对命令加共享密钥签名，不要执行收到的代码（不要对消息 `load`）。
- 不要把账号密码、令牌写进计算机文件或通过 HTTP 明文发送。
