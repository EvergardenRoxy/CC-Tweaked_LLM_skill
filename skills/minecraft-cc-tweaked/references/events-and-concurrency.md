# 事件、计时器与并发

> 来源：tweaked.cc 的 Events 页面、`os`、`parallel`、`_G.sleep` 文档与 "CraftOS's exception protocol" 参考。

## 目录

- 事件模型
- 全部事件一览
- 事件循环模式
- 计时器与闹钟
- `parallel`
- 外设调用会丢事件：看板 + 指令的标准结构
- 协程与自定义调度
- `terminate` 与退出
- 性能与"Too long without yielding"

---

## 事件模型

- 每台计算机有一个事件队列（最多 256 个，溢出丢弃）。
- `os.pullEvent(过滤)` 让出当前协程，直到出现**名字等于过滤**的事件；**不匹配的事件被丢弃**（对当前协程而言）。
- `os.pullEventRaw` 同上，但不会因 `terminate` 自动终止。注意 `terminate` **即使设置了过滤也会返回**，要自己判断。
- `sleep`、`rednet.receive`、`turtle.*`、外设方法、`http.get` 等内部都在 `pullEvent`，等待期间会吞掉其他事件。外设方法里最容易被忽略：通用外设（箱子/储罐/能量方块的 `list`、`size`、`getItemDetail`、`pushItems`、`tanks`、`getEnergy`……）和大多数模组外设的方法都要等服务器在下一个游戏刻执行完，**这段时间里到达的聊天、触摸、计时器事件会被当前协程丢掉**（见“外设调用会丢事件”一节）。显示器和终端的方法不等待。
- `parallel` 中每个函数有自己的事件副本，互不影响。

## 全部事件一览

| 事件 | 参数（事件名之后） | 触发时机 |
|---|---|---|
| `timer` | id | `os.startTimer` 到时 |
| `alarm` | id | `os.setAlarm` 到时 |
| `key` | 键码, 是否按住重复 | 按键（用 `keys.*` 常量比较） |
| `key_up` | 键码 | 松开按键 |
| `char` | 字符 | 输入可打印字符（文本输入用它，不用 `key`） |
| `paste` | 文本 | Ctrl+V 粘贴 |
| `mouse_click` | 按键(1左 2右 3中), x, y | 点击终端（仅高级设备） |
| `mouse_up` | 按键, x, y | 松开 |
| `mouse_drag` | 按键, x, y | 按住拖动 |
| `mouse_scroll` | 方向(-1 上, 1 下), x, y | 滚轮 |
| `monitor_touch` | 显示器名, x, y | 右键高级显示器 |
| `monitor_resize` | 显示器名 | 显示器尺寸变化 |
| `term_resize` | — | 主终端尺寸变化（需重绘） |
| `redstone` | — | 计算机或红石继电器的任一红石输入变化 |
| `peripheral` | 名字 | 外设接入 |
| `peripheral_detach` | 名字 | 外设断开 |
| `modem_message` | 调制解调器名, 信道, 回复信道, 消息, 距离 | 打开的信道收到消息 |
| `rednet_message` | 发送者ID, 消息, 协议 | rednet 消息 |
| `disk` / `disk_eject` | 驱动器名 | 插入 / 取出磁盘 |
| `turtle_inventory` | — | 海龟物品栏变化 |
| `speaker_audio_empty` | 扬声器名 | 扬声器可以接收更多音频 |
| `http_success` | url, 响应句柄 | 异步请求成功 |
| `http_failure` | url, 错误, 响应? | 异步请求失败 |
| `http_check` | url, 是否允许, 原因? | `checkURLAsync` 完成 |
| `websocket_success` | url, ws | WebSocket 连接成功 |
| `websocket_failure` | url, 错误 | 连接失败 |
| `websocket_message` | url, 内容, 是否二进制 | 收到消息 |
| `websocket_closed` | url, 原因?, 关闭码? | 连接关闭 |
| `task_complete` | 任务id, 成功, 错误或返回值… | `commands.execAsync` 等异步任务完成 |
| `setting_changed` | 名字, 新值, 旧值 | `settings.set` 等 |
| `computer_command` | 参数… | `/computercraft queue` 命令（命令计算机） |
| `file_transfer` | 文件列表对象 | 玩家把文件拖进计算机窗口 |
| `terminate` | — | 长按 Ctrl+T |

## 事件循环模式

```lua
-- 一个循环同时处理多种事件
local mon = peripheral.find("monitor")
local REFRESH = 2
local timer = os.startTimer(REFRESH)

local function redraw()
    if mon then
        mon.clear()
        mon.setCursorPos(1, 1)
        mon.write(os.date("%H:%M:%S"))
    end
end

redraw()
while true do
    local ev = { os.pullEvent() }
    local name = ev[1]
    if name == "timer" and ev[2] == timer then
        redraw()
        timer = os.startTimer(REFRESH)
    elseif name == "monitor_touch" then
        print("touch at", ev[3], ev[4])
    elseif name == "redstone" then
        print("redstone changed, back =", redstone.getInput("back"))
    elseif name == "key" and ev[2] == keys.q then
        break
    end
end
```

- `{ os.pullEvent() }` 把全部返回值装进表，适合事件参数个数不同的情况。`ev[1]` 是事件名，事件参数从 `ev[2]` 开始（上表“参数”一列的第 1 个是 `ev[2]`）。
- 这个结构只在**处理分支里没有会等待的外设调用**时才不丢事件。上例的 `redraw` 只调用显示器方法，所以没问题；如果计时器分支里还要读箱子或模组外设，改用下面“外设调用会丢事件”一节的结构。
- 每个计时器只触发一次；要周期执行就在处理时重新 `startTimer`。
- 比较计时器 ID，避免别的计时器（比如库内部的）误触发。

## 计时器与闹钟

| 函数 | 说明 |
|---|---|
| `os.startTimer(秒)` → id | 向上取整到 0.05 秒（游戏刻）；负数报错 |
| `os.cancelTimer(id)` | |
| `os.setAlarm(时间)` → id | 游戏内时间 0.0–24.0（如 `6.0` 为早上 6 点） |
| `os.cancelAlarm(id)` | |
| `os.clock()` | 计算机运行的游戏刻数 × 0.05：以 0.05 秒为单位前进；两次让出之间（一段连续执行的 Lua 里）不变；服务器卡顿时比真实时间慢 |
| `os.epoch("utc")` | 现实毫秒时间戳。判断“是否到时间了”、计算间隔和超时用它 |

## `parallel`

```lua
local function heartbeat()
    while true do
        print("alive", os.clock())
        sleep(5)
    end
end

local function listener()
    while true do
        local id, msg = rednet.receive("ctl")
        print("from", id, textutils.serialise(msg))
    end
end

local function quit_on_q()
    repeat
        local _, key = os.pullEvent("key")
    until key == keys.q
end

peripheral.find("modem", rednet.open)
parallel.waitForAny(heartbeat, listener, quit_on_q)
print("stopped")
```

- **传函数本身，不要传调用结果**：`parallel.waitForAny(heartbeat, listener)` ✓，`parallel.waitForAny(heartbeat(), listener())` ✗（会先在主线程里执行 `heartbeat()`，永远不返回）。
- 带参数的任务包一层：`function() worker(1) end`。
- 每个协程都会收到所有事件的副本：两个协程同时 `http.get` **同一 URL** 会拿到同一个响应，另一个响应无人认领。并发请求时让每个请求的 URL 各不相同（见 `app-engineering.md`）。
- `waitForAny`：任一结束即全部停止；`waitForAll`：等全部结束。任一报错会向上抛并停止其他任务。
- 1.120.0+ `waitForAll(function(spawn) spawn(f, ...) end)` 可动态添加任务。

**批量外设调用提速**：多数外设方法每次要等一个游戏刻，顺序执行 100 次约 5 秒。用 `waitForAll` 并发：

```lua
local invs = { peripheral.find("inventory") }
local results = {}
local tasks = {}
for i, inv in ipairs(invs) do
    tasks[#tasks + 1] = function()
        results[i] = inv.list()
    end
end
parallel.waitForAll(table.unpack(tasks))
print("scanned", #invs, "inventories")
```

上百个外设时分批（例如每批 64 个），避免事件队列（256）溢出导致卡住。

## 外设调用会丢事件：看板 + 指令的标准结构

一个协程在等外设方法返回时，只认这次调用的 `task_complete` 事件，别的事件对它来说就丢了。常见后果：

- **指令偶尔没反应**：聊天指令、显示器触摸正好在读箱子/外设的那一刻到达，被丢掉；
- **看板冻结**：计时器在外设调用期间到期，事件被丢，“收到计时器再设下一个”的循环从此再也等不到计时器。

在 cct-run（运行的是 CC: Tweaked 1.120.2 本身的代码）里实测：同一个单循环程序每 0.5 秒读一次箱子和外设，同时收 20 条聊天指令，只处理了 11 条，而且计时器第一次触发后就丢了，轮询从此停止；改成下面的三协程结构，20 条全部处理。在真实游戏里的两次联合测试中，两个 AI 写的 Create 工厂控制程序都遇到了这两个现象。

**结构**：把“等事件”和“调用会等待的外设方法”放进不同的协程。

- **监听协程**：只 `os.pullEvent()`，把指令放进队列，**不调用任何会等待的外设方法**，所以一个事件都不会丢；
- **工作协程**：从队列里取指令执行（可以调用外设方法）；每次等待前先检查队列，所以它忙的时候到达的唤醒事件丢了也没关系；
- **轮询协程**：定时读外设、更新状态和画面（可以用 `sleep`，丢事件不影响别人）。

`parallel` 里每个协程都会收到每个事件的副本，各自的等待互不影响，所以这样拆开后监听协程总能收到事件。

```lua
-- Dashboard + commands: three coroutines, so no command or timer is lost
-- while a peripheral method waits for the server.
local chest = peripheral.find("inventory") or error("No inventory found", 0)
local mon = peripheral.find("monitor") or error("No monitor attached", 0)
local OUTPUT_SIDE = "back"           -- redstone line that runs the machine

local state = { items = 0, running = false, handled = 0 }
local queue = {}                     -- commands waiting for the worker

local function draw()
    mon.clear()
    mon.setCursorPos(1, 1)
    mon.write(("Items %d"):format(state.items))
    mon.setCursorPos(1, 2)
    mon.write(state.running and "RUNNING" or "STOPPED")
    mon.setCursorPos(1, 3)
    mon.write(("Commands %d"):format(state.handled))
end

-- 1. Poller: reads peripherals (these calls wait a tick or more).
local function poller()
    while true do
        local n = 0
        for _, item in pairs(chest.list()) do n = n + item.count end
        state.items = n
        draw()
        sleep(1)
    end
end

-- 2. Listener: only takes events and queues them; it never calls a
--    peripheral method that waits, so it never misses an event.
local function listener()
    while true do
        local ev = { os.pullEvent() }
        if ev[1] == "monitor_touch" or ev[1] == "chat" then
            queue[#queue + 1] = ev
            os.queueEvent("work")
        end
    end
end

-- 3. Worker: runs queued commands. It checks the queue before every wait,
--    so a "work" event lost while it was busy does not lose a command.
local function worker()
    while true do
        while #queue > 0 do
            local ev = table.remove(queue, 1)
            if ev[1] == "monitor_touch" then
                state.running = not state.running
            elseif ev[1] == "chat" and ev[3] == "!stop" then
                state.running = false
            end
            redstone.setOutput(OUTPUT_SIDE, state.running)
            state.handled = state.handled + 1
            draw()
        end
        os.pullEvent("work")
    end
end

parallel.waitForAny(poller, listener, worker)
```

- 显示器和终端的方法不等待，可以在任何协程里画；共享的 `state`、`queue` 是普通表，协程之间不会被打断（只在让出时切换），不需要加锁。
- 不要在监听协程里调用 `chest.list()`、`setTargetSpeed`、`sendMessageToPlayer` 这类方法；要调用就放进队列交给工作协程。
- 只有显示器按钮、没有轮询外设的程序（如模板 8），单个事件循环就够了。

## 协程与自定义调度

可以直接用 `coroutine.create/resume/yield/status`。CraftOS 中 `coroutine.yield` 等同于等待事件：被调度的协程 yield 出来的值是它要等的**事件过滤名**，调度器应把匹配事件 resume 回去。除非确有需要，优先用 `parallel`。
在协程或 `parallel` 中出错时，CraftOS 的"异常"对象会保留出错位置；自写调度器可参考官方 exception protocol（带 `message`、`thread` 字段和 `__name = "exception"` 元表）。

## `terminate` 与退出

- 用户长按 Ctrl+T → `terminate` 事件；`os.pullEvent` 收到后抛出 `"Terminated"` 错误终止程序。
- 需要清理（关红石、存进度）时：

```lua
local function main()
    redstone.setOutput("back", true)
    while true do
        sleep(1)
    end
end

local ok, err = pcall(main)
redstone.setOutput("back", false)   -- 无论如何都关掉
if not ok and err ~= "Terminated" then printError(err) end
```

- 防止被 Ctrl+T 终止（如门锁）：用 `os.pullEventRaw` 并忽略 `terminate`，或临时 `os.pullEvent = os.pullEventRaw`（程序结束前恢复）。这会让程序很难停止，调试时别用。
- 退出程序：在主块里 `return`，或 `error("消息", 0)`（第二个参数 0 去掉文件名/行号前缀）。没有 `os.exit`。

## 性能与"Too long without yielding"

- 计算机长时间运行 Lua 代码而不让出时，会先被要求让出，再不让出就报 `Too long without yielding` 并终止。
- 纯计算的大循环中定期让出：

```lua
local function yield_now()
    os.queueEvent("yield")
    os.pullEvent("yield")
end

local sum = 0
for i = 1, 1000000 do
    sum = sum + i
    if i % 10000 == 0 then yield_now() end
end
print(sum)
```

- `sleep(0)` 也能让出，但至少等 0.05 秒；`queueEvent`+`pullEvent` 更快。
- 不要在循环里每次都 `getItemDetail` 扫描整个大仓库；先用 `list()`，必要时缓存详情。
- 服务器卡顿时可让管理员用 `/computercraft track` 找出占用最多的计算机（见 `config-and-versions.md`）。
