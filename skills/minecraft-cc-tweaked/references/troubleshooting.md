# 排错：常见错误、报错信息与排查流程

## 常见错误对照表

**报错** = 运行时出错停止；**语法错** = 程序一运行就报错（通常带 `:行号:`）；**语义错** = 不报错但行为不对。

| # | 错误写法 / 现象 | 类型 | 正确写法 / 说明 |
|---|---|---|---|
| 1 | `turtle:forward()`、`mon:write("x")`、`chest:list()` | 报错 | CC API 用 `.`：`turtle.forward()`；只有 io 句柄、vector 用 `:` |
| 2 | `peripheral.wrap("chest")` 返回 nil | 报错（后续 index nil） | 名字是方向或网络名（`"minecraft:chest_0"`）；用 `peripheral.getNames()` 查看 |
| 3 | 有线调制解调器没右键启用 | 报错/找不到外设 | 右键外设上的调制解调器，看到"Peripheral … connected"（名字）才算连接 |
| 4 | `for i, v in ipairs(chest.list())` | 语义错 | 空槽为 nil，`ipairs` 提前停止；用 `pairs` |
| 5 | `#chest.list()` 当物品数量 | 语义错 | 稀疏表长度不可靠；遍历累加 `count` |
| 6 | `pushItems(chestB, 1)`（传了 wrap 对象） | 报错 | 传名字：`peripheral.getName(chestB)` |
| 7 | 两个箱子贴在计算机两侧，`pushItems` 失败 | 报错 | 官方要求两个容器在同一有线网络上；都接上有线调制解调器 |
| 8 | `while true do … end` 里没有 yield | 报错 | `Too long without yielding`；加 `sleep`/`os.pullEvent` |
| 9 | 用 `sleep` 轮询时 rednet 消息/按键丢失 | 语义错 | `sleep` 丢弃事件；用事件循环或 `parallel` |
| 10 | `parallel.waitForAny(a(), b())` | 语义错/卡死 | 传函数本身：`parallel.waitForAny(a, b)` |
| 11 | 海龟不动 | 语义错 | 没燃料（`turtle.getFuelLevel()`）、被挡住、在区块边缘；打印 `turtle.forward()` 的第二个返回值 |
| 12 | `turtle.getFuelLevel() < 100` 报错 | 报错 | 燃料关闭时返回字符串 `"unlimited"`，先判断 |
| 13 | 挖沙砾/沙子的隧道中途卡住 | 语义错 | `while turtle.detect() do turtle.dig() end` |
| 14 | 海龟 `dig` 返回 false | 语义错 | 没装能挖的工具、方块不可破坏（基岩）、受保护区域 |
| 15 | 海龟 `place` 放不下 | 语义错 | 当前槽为空/不是方块、前方被占；先 `select` |
| 16 | 海龟坐标"漂移" | 语义错 | 移动失败时也更新了坐标；只在返回 true 后更新 |
| 17 | 程序重进世界后停了 | 语义错 | 区块卸载会关机；写 `startup.lua` 自启，进度存文件 |
| 18 | `a // b`、`x & 1`、`1 << 4` | 语法错 | Lua 5.2：`math.floor(a / b)`、`bit32.band(x, 1)`、`bit32.lshift(1, 4)` |
| 19 | `if a != b`、`a += 1`、`x++`、`//` 注释 | 语法错 | `~=`、`a = a + 1`、注释用 `--` |
| 20 | `"a" + "b"` 拼接字符串 | 报错 | 用 `..` |
| 21 | `os.exit()`、`os.execute()`、`collectgarbage()` | 报错 | 不存在；退出用 `return`/`error("…", 0)` |
| 22 | `string.format("%d", 2.5)` 期望四舍五入 | 语义错 | 先 `math.floor(x + 0.5)` |
| 23 | `fs.open("data.txt")` 读不到当前目录文件 | 语义错 | `fs` 不看 shell 当前目录；写绝对路径或 `shell.resolve` |
| 24 | 写文件后内容为空 | 语义错 | 忘了 `h.close()` |
| 25 | `textutils.unserialise` 返回 nil | 语义错 | 内容不是合法 Lua 字面量（可能写入时没 serialise）；先打印原文 |
| 26 | `require("lib/util.lua")` 找不到 | 报错 | `require("lib.util")`，相对当前程序目录 |
| 27 | 普通计算机/显示器上颜色不显示 | 语义错 | 只显示灰度；需要高级设备 |
| 28 | `os.pullEvent("monitor_touch")` 永远不触发 | 语义错 | 只有高级显示器可触摸；确认点的是显示器正面 |
| 29 | 显示器文字超出或乱 | 语义错 | `mon.write` 不折行；每次重绘前 `mon.clear()`，用 `mon.getSize()` 截断 |
| 30 | `rednet.receive()` 收不到 | 语义错 | 两端都 `rednet.open`；距离 > 64（无线）；协议名不一致；对方发的是 `modem.transmit` 而不是 rednet |
| 31 | `gps.locate()` 返回 nil | 语义错 | 星座不足 4 台/未运行/不在范围；本机没装无线调制解调器 |
| 32 | `http` 是 nil 或请求被拒 | 报错 | 服务器关闭了 HTTP，或域名/局域网地址被规则禁止 |
| 33 | `commands` 是 nil | 报错 | 只有命令计算机有 `commands` API |
| 34 | `turtle` 是 nil | 报错 | 程序跑在普通计算机上 |
| 35 | 改了 `startup.lua` 后无法进入系统 | 卡死 | 长按 Ctrl+T；无效时用带空 `startup.lua` 的软盘从磁盘驱动器启动 |
| 36 | 扬声器 `playAudio` 断断续续 | 语义错 | 每次多给样本（最多 128×1024），返回 false 时等 `speaker_audio_empty` |
| 37 | 事件参数取错（如 `monitor_touch` 把名字当 x） | 语义错 | 对照 `events-and-concurrency.md` 的参数顺序 |
| 38 | `settings.set` 后重启丢失 | 语义错 | 需要 `settings.save()` |
| 39 | `print("你好")` 显示乱码，`#"你好"` 等于 6 | 语义错 | CC 终端只有自带的 256 个字符，不能直接显示中文；默认用英文/拼音；用户确认需要中文时用 utf8display 点阵字体库（见 `app-engineering.md`）；字符数用 `utf8.len` |
| 40 | 多台扬声器播放不同步/有杂音 | 语义错 | 同一块数据发给所有扬声器，全部接受后才送下一块；一条流一个解码器，跳转后重建解码器 |
| 41 | 下载大文件被截断或失败 | 报错 | 超过服务器 `max_download`（默认约 16 MiB）；用 Range 分段下载 |
| 42 | 并发请求时响应"串台"或某个请求永远不返回 | 语义错 | 同一 URL 同时请求会抢事件；给每个请求加唯一标记参数，并为每个请求设超时看门狗 |
| 43 | 安装/更新中途断网，程序文件新旧混杂无法启动 | 语义错 | 先把全部文件下载到内存并校验，再统一写入（见 `app-engineering.md`） |
| 44 | 程序退出后屏幕颜色仍然不对 | 语义错 | 改过调色板要在退出（含报错、Ctrl+T）时恢复；或重启计算机 |
| 45 | 配置文件损坏导致程序启动即崩溃 | 报错 | 读取时 `pcall`/校验每个字段，失败回退默认值并提示 |
| 46 | 照教程写 `textutils.sha256(...)` 报 `attempt to call nil` | 报错 | CC 没有内置哈希/加密；用经过测试的纯 Lua 实现（`security.md`） |
| 47 | 安全终端里 `os.run` 启动的程序调用 `shell.run` 报错，然后掉回 shell | 报错 | `os.run` 不提供 `shell`；主循环用 `pcall` 包住且永不返回 |
| 48 | 设了 `os.pullEvent = os.pullEventRaw` 仍被人进入 shell | 语义错 | Ctrl+R/Ctrl+S 无法拦截、软盘可抢先启动；启动文件本身要是锁，并禁用磁盘启动 |
| 49 | 程序里多处 `os.pullEvent(过滤)`/`sleep`，计时器偶尔"失效"不再触发 | 语义错 | 计时器事件被别处的等待吞掉；改为单一事件等待点 + 每轮检查重新武装计时器 |
| 50 | 服务器卡顿时音频/同步逻辑越来越慢、延迟越积越大 | 语义错 | 按刻数计时会随 TPS 变慢；改用 `os.epoch("utc")` 计算节拍，并限制缓冲长度 |
| 51 | 新手在 shell 输入 `turtle.forward()` 报 `No such program` | 语义错 | shell 只运行程序；先输入 `lua` 进入交互环境（见 `getting-started.md`） |

## 报错信息速查

报错格式通常是 `文件名:行号: 消息`。先看行号对应的代码。

| 报错（原文片段） | 含义与处理 |
|---|---|
| `attempt to index ... (a nil value)` | 对 nil 取字段：通常是 `peripheral.wrap/find` 没找到、`fs.open`/`http.get` 失败、表里没有这个键。检查前一步的返回值 |
| `attempt to call ... (a nil value)` | 调用不存在的函数：函数名拼错、API 在此设备上不存在（`turtle`/`commands`/`pocket`/`multishell`）、外设没有这个方法（`peripheral.getMethods` 查）、函数定义在调用之后 |
| `attempt to compare number with nil` / `string with number` | 比较前变量为 nil 或类型不同（如燃料 `"unlimited"`、`tonumber` 失败） |
| `attempt to perform arithmetic on ... (a nil value)` | 参与运算的值为 nil；常见于命令行参数未传 |
| `attempt to concatenate ... (a nil value)` | `..` 两边有 nil；用 `tostring(x)` |
| `bad argument #N to 'xxx' (Y expected, got Z)` | 第 N 个参数类型不对；对照 API 签名（槽位要数字、名字要字符串） |
| `Too long without yielding` | 循环里没有让出；见 `events-and-concurrency.md` 最后一节 |
| `Terminated` | 用户按了 Ctrl+T（正常） |
| `No such program` | shell 找不到程序：文件名拼错、不在当前目录/路径；用 `ls` 查看 |
| `No such modem: xxx` | `rednet.open` 的名字不是调制解调器 |
| `'end' expected (to close 'function' at line N) near <eof>` | 少了 `end`；从第 N 行开始数配对 |
| `unexpected symbol near 'x'` / `'=' expected near 'x'` | 语法错：使用了其他语言的写法（`!=`、`+=`、`//`、`{}` 代码块、缺 `then`/`do`） |
| `Domain not permitted` 等 HTTP 错误 | 服务器 HTTP 规则拒绝；见 `config-and-versions.md` |
| 海龟返回的原因字符串 | 例如 `Movement obstructed`（被挡）、`Out of fuel`（没燃料）、`Nothing to dig here`（前方无方块）；原文随版本可能不同，**让用户打印第二个返回值** |

## 排错流程

1. **拿到完整报错**：文件名、行号、消息原文；或者描述"做了什么、期望什么、实际发生什么"。
2. **确认环境**：`print(_HOST)`（版本）、设备类型（普通/高级/海龟）、`peripheral.getNames()` 与 `peripheral.getType(名)`。
3. **最小化**：在 `lua` 交互环境中单独执行可疑的那一行（例如 `peripheral.wrap("minecraft:chest_0").list()`），看返回值。
4. **打印中间值**：`print(textutils.serialise(x))` 或 `require("cc.pretty").pretty_print(x)`；海龟动作打印 `print(turtle.forward())` 看原因。
5. **检查是否让出 / 是否丢事件**：循环结构、`sleep` 与事件混用。
6. **检查服务器配置**：HTTP、燃料、命令方块、磁盘空间（`fs.getFreeSpace("/")`）。
7. 修好后，用第 6 节自检清单（SKILL.md）复核整个程序。

## 游戏内工具

| 工具 | 用途 |
|---|---|
| `lua` | 交互式 Lua；可直接试 API、查看返回值（自动打印表达式结果） |
| `peripherals` | 列出所有外设名 |
| `programs` / `ls` / `cd` / `edit` / `rm` / `mv` / `cp` | 程序列表与文件操作 |
| `help <主题>` | 内置帮助（如 `help turtle`） |
| `label set <名字>` / `id` | 设置标签 / 查看 ID |
| `set <设置名> <值>` | 修改 settings |
| `wget` / `pastebin` | 下载程序（需 HTTP） |
| `monitor <显示器名> <程序>` | 在显示器上运行程序 |
| `/computercraft dump` / `view` / `track` | 管理员命令：列出计算机、远程查看终端、性能分析（见 `config-and-versions.md`） |
