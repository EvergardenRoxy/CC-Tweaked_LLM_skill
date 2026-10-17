---
name: minecraft-cc-tweaked
description: 协助用户为 Minecraft 模组 CC：Tweaked（ComputerCraft，CC:T，CraftOS）编写、审查、调试 Lua 程序：计算机、海龟（turtle）、口袋计算机、命令计算机，以及显示器、调制解调器、箱子/储罐/能量方块、扬声器、打印机、磁盘驱动器、红石继电器等外设，和 Create、Advanced Peripherals 等模组提供的外设；rednet/GPS 网络、红石控制、HTTP/WebSocket、显示器界面。当用户提到 CC: Tweaked、ComputerCraft、CC:T、CraftOS、海龟/turtle、rednet、peripheral.wrap/find、startup.lua、monitor 显示器、有线调制解调器、pastebin/wget，或要求用 Lua 在 Minecraft 里自动化挖矿、种植、仓储、监控、工厂控制、远程控制时使用。
---

# Minecraft CC: Tweaked（ComputerCraft）编程协助指南

本 Skill 是编写 CC: Tweaked 程序时的**权威参考**，内容以官方文档 <https://tweaked.cc> 和实测为准。CC: Tweaked 的 Lua 环境与普通 Lua 有不少差别（Lua 5.2 运行时、事件驱动、外设命名、海龟燃料……），网上还有大量旧版 ComputerCraft（1.7.10 时代）的过时写法。**你记忆里的 CC 写法可能是错的或过时的，必须以本 Skill 和 tweaked.cc 为准。**

本文件是常驻的核心部分（规则、流程、执行模型、速查、自检清单）。细节放在 `references/` 中，按第 1 节的索引**按需读取**；本文件没写到的细节，先读对应的文件再回答。

**本 Skill 的用法：先拆解、先对齐，再写码。** 收到请求后先拆解问题、想出最简单可行的方案，和用户确认目标（第 2.0 节），再按 2.2 节从约束推导结构与失败处理。`templates.md` 里的程序只是某组约束下的一个答案，用来核对写法，**不要把模板改改名字就交付**。

---

## 0. 给 AI 的铁律（先读这一节）

0. **先拆解问题、先给最简单的方案、先和用户对齐目标，再写复杂代码**（第 2.0 节）。能用现成程序（`excavate`、`tunnel`、`go`）、原版红石/漏斗或二十行脚本解决的，就不要写大程序。用户没要求的功能（图形界面、日志、配置文件、重试框架、认证）只列为"可选增强"。
1. **运行时是 Lua 5.2（Cobalt）。** 没有整数子类型、`//`、位运算符 `& | ~ << >>`（用 `bit32.*`）、`collectgarbage`、`os.execute`、`os.exit`、`os.getenv`、`io.popen`。`goto`、`table.unpack`、`utf8`、`string.pack` 可用。见第 4.1 节。
2. **只使用真实存在的 API，并分清 CC: Tweaked 本体和模组。** 本体 API 以 tweaked.cc 和 `api-reference.md` 为准；Create、Advanced Peripherals 等**模组**的外设方法各版本不同，以用户游戏里 `peripheral.getMethods("名字")` 的结果为准，本 Skill 的实测记录在 `mod-*.md`（标明了模组和版本）。不确定就让用户在 `lua` 里查，**不要编造函数**，也不要把模组的行为当成 CC 本体的行为。
3. **CC 的 API 一律用 `.` 调用**：`turtle.forward()`、`peripheral.wrap("top")`、`chest.list()`、`mon.write("x")`。只有 `io` 文件句柄（`f:read("l")`）和 `vector` 对象用 `:`。
4. **外设名字只有两种**：相邻方块用方向 `"top" "bottom" "left" "right" "front" "back"`；经有线调制解调器连接的用网络名，如 `"minecraft:chest_0"`。不要编造名字；优先 `peripheral.find("类型")`，**检查返回 nil** 后用 `error("…", 0)` 给出清楚提示。
5. **会失败的操作要检查返回值。** 海龟动作失败时**不抛错**，返回 `false, "原因"`；`fs.open`、`http.get`、`peripheral.wrap`、`rednet.receive(超时)` 失败返回 `nil`。
6. **长时间运行的循环必须让出（yield）**：循环里要有 `os.pullEvent`/`sleep`/海龟动作/外设调用，否则 `Too long without yielding`。
7. **`sleep()`、带过滤的 `os.pullEvent`、会等待的外设方法都会丢弃等待期间到来的其他事件。** 箱子/储罐/能量方块的通用方法和大多数模组外设方法都要等服务器执行。**既要轮询外设又要响应指令/触摸**（看板、工厂控制），用 `parallel` 把只收事件的监听协程和调用外设的协程分开（第 3 节、`events-and-concurrency.md`）。
8. **`inventory.list()`、`fluid_storage.tanks()` 返回稀疏表**，用 `pairs`；`pushItems`/`pullItems` 的第一个参数是对方外设的**名字字符串**，两个容器要在同一个有线网络上。
9. **海龟移动消耗燃料**（转向不耗）。开头检查 `turtle.getFuelLevel()`（可能是 `"unlimited"`）；处理沙砾掉落、生物挡路、背包满、返回路径的燃料。
10. **计算机所在区块卸载时会关机，变量全部丢失。** 需要自启就写启动文件，需要续跑就把进度写进文件。**用户已有 `startup.lua` 时不要覆盖**：把你的启动器放进 `/startup/` 目录，两者开机时都会运行。
11. **版本不确定时先问版本**（`print(_HOST)`）。版本敏感特性见第 4.4 节。
12. **给出的程序必须附"安装清单"**（设备、外设位置或网络名、文件路径、运行方法），交付前逐条过第 6 节自检清单。
13. **CC 的终端和显示器不能显示中文。** 界面文字、`print`/`error` 信息一律用英文或拼音，并告诉用户原因；代码注释可以用中文。需要中文时（中文界面、聊天框收发中文、Create 显示板），先读 `chinese-text.md`：每条途径都有前提，有的只在特定模组上可用。
14. **只有在用户确实需要并同意时，才把程序写成大型工程**（长期运行、联网、带界面），按 `app-engineering.md` 的规范；显示器界面按 `ui-design.md`。
15. **不照搬模板、教程或记忆中的代码。** 网上教程常含不存在的函数（如 `textutils.sha256`）和错误的环境假设；逐个函数核对，按 `design-thinking.md` 第六节评审。
16. **安全认证代码只在用户同意后才加入。** 默认在风险提示里用一两句话说明风险和可选方案；用户要求门禁、密码、权限时，先确认威胁模型，再按 `security.md` 选机制。任何情况下都不要执行收到的消息内容（`load` 网络数据）。
17. **能测就先测，没测过就不要说“测试通过”。** 工具列表里有 `cct_run`（可能带前缀）或 `cct_live_*` 时，交付前按 `testing.md` 运行并如实写出结果和没覆盖的部分；没有时，第一次交付时提醒一次可以安装测试环境。

---

## 1. 参考文件索引（按需读取）

| 遇到这种情况 | 必须先读 |
|---|---|
| **任何新需求的设计阶段**：从需求推导结构、CC 的硬约束、失败模式分析、思路模式库、评审别人代码的方法 | `references/design-thinking.md` |
| 要用第 4 节没列出的函数，或需要确切的参数/返回值（`fs`、`term`、`textutils`、`settings`、`http`、`os`、`colors`、`window`、`cc.*`……） | `references/api-reference.md` |
| CC 本体的外设：箱子/储罐/能量方块、显示器、扬声器、打印机、磁盘驱动器、红石继电器、命令方块；有线网络命名；物品/方块详情字段；**模组外设的通用排查方法** | `references/peripherals.md` |
| **Create（机械动力）模组**的外设：应力表、转速表、转速控制器、显示链接器（显示板）、物品保险库；离合器等机械行为 | `references/mod-create.md` |
| **Advanced Peripherals 模组**的外设：聊天框、玩家探测器 | `references/mod-advanced-peripherals.md` |
| 任何**中文**：中文界面、聊天框收发中文、Create 显示板显示中文、字符串长度与编码、测试里注入中文 | `references/chinese-text.md` |
| **显示器界面**：布局、侧边栏、按钮与触摸、进度条对齐、绘图字符、调色板、刷新与防闪烁、让用户截图确认 | `references/ui-design.md` |
| 写海龟程序：挖矿、隧道、砍树、种田、建造、合成、坐标与朝向跟踪 | `references/turtle.md` |
| 计算机间通信（rednet/modem）、GPS、HTTP/WebSocket、下载程序 | `references/networking.md` |
| 事件循环、定时器、`parallel`、协程、触摸、`terminate`；**看板 + 指令类程序的结构** | `references/events-and-concurrency.md` |
| 想找相似案例（仓储统计、自动熔炉、伐木、隧道、远程控制、触摸按钮、能量监控、音乐……） | `references/templates.md` |
| 用户贴出报错原文，或说"不工作/没反应/卡住/报错" | `references/troubleshooting.md` |
| 服务器配置（HTTP 白名单、磁盘空间、燃料）、`/computercraft` 命令、版本差异、Lua 兼容性 | `references/config-and-versions.md` |
| 写几百行以上的应用：模块结构、可靠 HTTP、安装器/更新器、设置持久化、外设热插拔、日志、发布 | `references/app-engineering.md` |
| 密码、登录终端、门禁、权限、加密、远程认证 | `references/security.md` |
| 新手问题：在哪里输入代码、`No such program`、怎么读文档签名、外部编辑器、中文资料的可信度 | `references/getting-started.md` |
| **交付前测试程序**、重现用户的报错；工具列表里有 `cct_run` / `cct_live_*`；或者要提醒用户安装测试环境 | `references/testing.md` |

---

## 2. 协助流程

### 2.0 先拆解、先对齐目标（收到请求后的第一步）

1. **复述目标**：用一句话说出用户想达成的结果（而不是用户提到的手段）。
2. **拆解**：输入从哪来、要做什么、输出到哪、多久一次、出错怎么办。
3. **从简单到复杂列方案**：不写代码（原版红石/漏斗、已装模组的功能、ROM 自带程序）→ 几十行的单文件脚本 → 多文件、带界面/配置/网络协议的系统。
4. **推荐能满足目标的最简单方案**，说明局限和以后往哪扩展。
5. **只问会改变方案的问题**，合并成一条消息，并给出默认假设。
6. **用户确认后再写代码**。

请求小而明确、改动范围清楚的修 bug、用户已给出完整需求并要求直接写时，可以跳过协商，但要在回答开头写明假设。**复杂度预算**：用户没要求的功能放进"可选增强"。

### 2.1 先问清的信息（缺失才问，已知就不要再问）

| 要确认的信息 | 为什么重要 |
|---|---|
| CC: Tweaked 版本、Minecraft 版本、加载器 | 部分 API 随版本增加；旧版 ComputerCraft（1.7.10/1.12）差别很大 |
| 设备类型：普通/高级计算机、海龟、口袋计算机、命令计算机 | 颜色、鼠标事件、燃料上限、`commands` API 只在特定设备上可用 |
| 外设及连接方式：贴在哪一面，还是有线网络 | 决定外设名字和能否 `pushItems` |
| 涉及的模组方块及**模组版本**（Create、Advanced Peripherals、Mekanism、AE2……） | 模组外设的类型名、方法和行为随模组和版本变化 |
| 是否开机自启、是否要在区块卸载后继续；已有的 `startup.lua` | 启动方式与进度持久化 |
| 是否多人服务器、HTTP 是否开放 | `http`/`wget`/`pastebin` 可能被禁用 |
| 现有代码、报错原文（含文件名和行号） | 排错必需 |

### 2.2 设计步骤（详见 `references/design-thinking.md`）

1. **翻译成 CC 原语**：输入（事件、轮询外设、红石、网络、计时器）、输出、要持久化的状态。
2. **列约束**：时间粒度、外设调用耗时、事件丢失、区块加载、外设变化、网络不可靠、磁盘/内存、字符集、谁能接触机器。
3. **选结构**：一次性脚本 / 轮询循环 / 事件循环 / `parallel` 多任务 / 状态机 / 多台计算机，并说出理由。
4. **失败模式**：对每个外部交互问"失败、不返回、对象消失、重复乱序、做了没生效"怎么办。
5. **可观测性与验证**：启动自检、状态显示、日志；规划用户一步步验证的方法。
6. 写代码，过第 6 节自检清单；有测试环境就先按 2.4 节测试，再按 2.3 节交付。

### 2.3 回答格式模板

**第一轮（需求不够明确或方案不止一种时）：先对齐，不写完整代码**

````text
【我理解的目标】……
【拆解】1. … 2. … 3. …
【可选方案】
  A（最简单）：……  优点/局限
  B：……            优点/局限
【我的建议】A，因为……；以后需要……再升级到 B。
【需要你确认】（只列会改变方案的问题，附默认假设）
  1. ……（默认：……）
````

**确认后：交付程序**

````text
【整体思路】一两句话说明程序做什么、怎么循环。
【关键设计决策】为什么选这种结构；处理了哪些失败情况；哪些条件变了需要改哪里。
【安装清单】
| 设备/外设 | 位置或网络名 | 说明 |
| 高级计算机 | — | 运行本程序 |
| 显示器 3×2 | 计算机 top 面 | 显示统计 |
| 箱子 ×N | 有线调制解调器 → minecraft:chest_0… | 右键调制解调器启用连接 |
【程序】保存为 /startup.lua（或 /程序名.lua）
```lua
...
```
【怎么装、怎么跑】放好设备；`edit 文件名` 粘贴保存，或 `wget`/`pastebin get`；运行或 `reboot`；Ctrl+T 终止、Ctrl+R 重启（长按）。
【怎么验证】先在 `lua` 里验证哪几个调用；运行后看到什么说明正常。
（有测试环境时）【测试】测了哪些情况、结果如何；分清实机真实发生 / 实机注入 / 只在模拟器 / 没测。
【风险提示】燃料/区块加载/外设名字/服务器配置/性能/安全……
【可选增强】用户没要求、所以没写进代码的功能——需要哪个告诉我
````

### 2.4 测试（详见 `references/testing.md`）

| 情况 | 怎么做 |
|---|---|
| **只有本 Skill**（没有 `cct_run` 等工具，也没有 `cct-run` 命令） | 按自检清单检查后交付；第一次交付时提醒一次可以安装 cct-run；不要写“已测试” |
| **有模拟器**（`cct_run`、`cct_trace`、`cct_screen`、`cct_guide`，或命令行 `cct-run`） | 用符合用户真实布局的 fixture 运行（模组外设用实机数值写成 `scripted`），读 `status`、报错行号和 trace，修到通过；有并行结构时用一串紧挨着的指令验证没有丢事件 |
| **还有实机工具**（`cct_live_*`） | 只在用户同意时接管指定的电脑；改文件前先快照，测完恢复并释放；聊天、过载等要请用户真的做一次，注入的事件不算实机验证；界面好不好看请用户截图 |

---

## 3. 核心概念与执行模型

- **计算机**：开机运行 CraftOS（`bios.lua` → `shell`），然后执行启动文件（`startup.lua`，以及 `startup/` 目录下的全部文件，按文件名排序），再进入命令行。普通计算机只有灰度，**高级**计算机有 16 色和鼠标事件。
- **海龟**：带 16 格物品栏、可移动的计算机，左右各一个升级槽。**口袋计算机**有 `pocket` API。**命令计算机**有 `commands` API。
- **文件系统**：每台计算机有独立硬盘（默认约 1 MB），`/rom` 只读，软盘挂载在 `/disk` 等目录。

**执行模型**（最重要）：

```text
每台计算机 = 一个 Lua 程序在协程里运行，靠"事件"驱动：
  os.pullEvent(过滤)   → 让出（yield），直到队列里出现匹配的事件才继续
  sleep(n)            → 内部 = startTimer + 只等这个 timer 事件；等待期间其他事件被丢弃
  外设方法/海龟动作     → 内部也会让出，等服务器在游戏刻里执行完再返回（通常 ≥ 1 刻 = 0.05 秒）；
                         等待期间到达的其他事件同样被丢弃（显示器、终端方法除外，它们不等待）
  事件队列最多 256 个；溢出的事件被丢弃
  长时间不让出         → "Too long without yielding"，程序被终止
```

- 程序**不会**真正并行；`parallel.waitForAny/All` 在多个协程间切换，一个协程让出时另一个才运行。
- 时间单位是**秒**，精度 0.05 秒（1 游戏刻）。

| 需求 | 写法 |
|---|---|
| 每 N 秒做一次，不需要响应输入 | `while true do 工作() sleep(N) end` |
| 等某种事件（触摸、消息、红石变化） | `while true do local e, a, b = os.pullEvent("monitor_touch") … end` |
| 定时 + 响应事件（处理时不调用会等待的外设方法） | `os.startTimer` 事件循环（下例） |
| 轮询箱子/模组外设 + 响应聊天指令、触摸 | `parallel` 三协程：监听协程只收事件放进队列，工作协程执行，轮询协程读外设（模板见 `events-and-concurrency.md`；单个循环会丢指令、冻结看板） |
| 批量调用外设方法提速 | 把调用包成函数列表交给 `parallel.waitForAll` |

```lua
local INTERVAL = 5
local timer = os.startTimer(INTERVAL)
while true do
    local event, p1 = os.pullEvent()
    if event == "timer" and p1 == timer then
        print("tick", os.clock())
        timer = os.startTimer(INTERVAL)
    elseif event == "key" and p1 == keys.q then
        print("bye")
        break
    end
end
```

---

## 4. 语言与 API 速查

### 4.1 Lua 5.2（Cobalt）与 CraftOS 的差别

| 写法 | 在 CC: Tweaked 中 |
|---|---|
| `a // b`、`a & b`、`a << 2`、`~a` | **语法错误**。用 `math.floor(a / b)`、`bit32.band(a, b)`、`bit32.lshift(a, 2)`、`bit32.bnot(a)` |
| `math.type`、`math.tointeger`、`math.maxinteger` | 不存在（数字都是浮点） |
| `string.format("%d", x)` | `x` 是小数时先 `math.floor(x)`，或用 `%.1f` |
| `collectgarbage`、`os.execute`、`os.exit`、`os.getenv`、`os.remove`、`io.popen` | 不存在。删文件用 `fs.delete`，退出用 `return` 或 `error("…", 0)` |
| `goto`、`table.unpack`、`table.pack`、`select("#", …)`、`load(str, name, "t", env)` | 可用 |
| `setfenv`/`getfenv` | 不要依赖；用 `load` 的 `env` 参数 |
| `require("mod")` | 可用；**相对当前程序目录**搜索；子目录写 `require("a.b")` |
| 一个函数里超过 200 个 `local` | 编译错误；拆成模块表和多个文件（`app-engineering.md`） |
| `...` | 程序的命令行参数：`local a, b = ...` |

### 4.2 外设基础

```lua
local mon = peripheral.find("monitor")                  -- 任意一个显示器
local chest = peripheral.wrap("minecraft:chest_0")      -- 按名字
if not chest then error("minecraft:chest_0 not found; is the wired modem enabled?", 0) end
local drives = { peripheral.find("drive") }             -- 全部驱动器（多返回值用表接住）
for _, name in ipairs(peripheral.getNames()) do print(name, peripheral.getType(name)) end
```

| 函数 | 说明 |
|---|---|
| `peripheral.getNames()` / `isPresent(名)` / `getType(名或对象)` / `hasType(x, 类型)` | 所有外设名 / 是否存在 / 类型（可能多个）/ 是否某类型 |
| `peripheral.getMethods(名)` | 方法名列表——**不确定外设（尤其是模组外设）有什么方法时让用户跑这个** |
| `peripheral.wrap(名)` / `find(类型 [, 过滤])` / `call(名, 方法, ...)` / `getName(对象)` | 包装（不存在返回 `nil`）/ 查找全部匹配 / 直接调用 / 对象 → 名字 |

有线网络：计算机和每个外设各贴一个**有线调制解调器**，用网线连起来，**右键调制解调器**使其连接（变红并在聊天栏显示名字）。接入/断开触发 `peripheral` / `peripheral_detach` 事件。

### 4.3 常用写法速查（细节见括号里的文件）

| 主题 | 写法 |
|---|---|
| 物品栏（`peripherals.md`） | `for slot, item in pairs(inv.list()) do … end`；`inv.pushItems(peripheral.getName(other), slot [, n])`；`size()`、`getItemDetail(slot)` |
| 流体 / 能量 | `tanks()`（稀疏表，mB）、`pushFluid(名 [, 量])`；`getEnergy()`、`getEnergyCapacity()`（FE） |
| 海龟（`turtle.md`） | `turtle.forward()` 返回 `ok, 原因`；`while turtle.detect() do turtle.dig() end` 防沙砾；`turtle.refuel(0)` 检查是否可作燃料 |
| 红石 | `redstone.setOutput("back", true)`、`setAnalogOutput("top", 7)`、`getInput("left")`；`os.pullEvent("redstone")`；远处的红石用红石继电器 `redstone_relay`（1.114.0+） |
| 网络（`networking.md`） | `peripheral.find("modem", rednet.open)`；`rednet.send(id, 表, "协议")`；`rednet.receive("协议", 超时)`；rednet 不加密 |
| 显示器（`ui-design.md`） | `mon.setTextScale(0.5)`（0.5–5）；`mon.setCursorPos(1, 1)`、`mon.write("x")`（不折行）；`term.redirect(mon)` 后可 `print`；触摸只有高级显示器：`monitor_touch, 名字, x, y` |
| 文件与设置（`api-reference.md`） | 路径都是绝对路径；`fs.combine(a, b)`；表 ↔ 字符串用 `textutils.serialise`/`unserialise`，JSON 用 `serialiseJSON`/`unserialiseJSON` |
| 启动 | 启动顺序：`/rom/autorun` → 磁盘启动文件（需 `shell.allow_disk_startup`）→ 根目录 `startup.lua` 和 `startup/*`；`shell.run("程序", "参数")`；`os.setComputerLabel("名字")` |

```lua
-- Save and load program state (progress that must survive a restart).
local function save(path, state)
    local h = fs.open(path, "w")
    if not h then return false end
    h.write(textutils.serialise(state))
    h.close()
    return true
end

local function load_state(path, default)
    local h = fs.open(path, "r")
    if not h then return default end
    local state = textutils.unserialise(h.readAll())
    h.close()
    return type(state) == "table" and state or default
end

local state = load_state("/data/state.txt", { done = 0 })
state.done = state.done + 1
save("/data/state.txt", state)
settings.define("mine.depth", { description = "Mining depth", default = 32, type = "number" })
print(state.done, settings.get("mine.depth"))
```

### 4.4 版本敏感特性（用到前确认版本）

| 特性 | 版本 |
|---|---|
| 通用外设 `inventory`/`fluid_storage`/`energy_storage` | 1.94.0+ |
| 外设多类型、`peripheral.hasType` | 1.99+ |
| `speaker.playAudio`、`cc.audio.dfpwm` | 1.100+ |
| Lua 5.2 运行时、`fs.open` 的 `r+`/`w+` | 1.109.0+ |
| 红石继电器 `redstone_relay` | 1.114.0+ |
| `turtle.getEquippedLeft/Right` | 1.116.0+ |
| `cc.base64`、`commands.getDimension` | 1.119.0+ |
| `parallel.waitForAll` 的 `spawn` 参数 | 1.120.0+ |
| `turtle_storage` | 1.121.0+ |

完整列表见 `references/config-and-versions.md`。模组的版本差异见对应的 `mod-*.md`。

---

## 5. 最常见的错误

| 错误写法 | 后果 | 正确写法 |
|---|---|---|
| `turtle:forward()`、`mon:write("x")` | `bad argument` 报错 | `turtle.forward()`、`mon.write("x")` |
| `peripheral.wrap("chest")` | 返回 `nil`，后面 `attempt to index` | 用真实名字，或 `peripheral.find("inventory")` |
| `for i, item in ipairs(chest.list())` | 遇到第一个空槽就停止 | `pairs` |
| `chest.pushItems(other, slot)`（`other` 是对象） | 报错 | `chest.pushItems(peripheral.getName(other), slot)` |
| `while true do if rs.getInput("top") then … end end` | `Too long without yielding` | 循环里 `os.pullEvent("redstone")` 或 `sleep(…)` |
| `sleep(5)` 期间等 rednet 消息 | 消息被丢弃 | `rednet.receive(协议, 超时)` 或 `parallel` |
| 一个事件循环里既处理聊天/触摸，又调用 `chest.list()` 或模组外设方法 | 指令偶尔丢失；计时器丢失后看板冻结 | `parallel` 三协程（第 3 节） |
| `turtle.forward()` 不检查返回 | 撞墙/没燃料后坐标错乱 | `if not turtle.forward() then … end` |
| `if turtle.getFuelLevel() < 100` | 燃料无限时比较字符串报错 | 先判断 `== "unlimited"` |
| `mon.write("库存")`、`print("你好")` | 屏幕上是乱码 | 英文；需要中文见 `chinese-text.md` |
| 把中文字符串直接传给模组外设（聊天框、显示链接器） | 游戏里显示乱码 | 按 `chinese-text.md` 里各模组实测可用的写法 |
| 覆盖用户的 `startup.lua` | 用户原来的启动程序没了 | 启动器放进 `/startup/` 目录 |
| `startup.lua` 有 bug 或死循环 | 每次开机都崩/卡住 | 先手动运行测试；卡住时长按 Ctrl+T；无效时用带空 `startup.lua` 的软盘启动 |

更多见 `references/troubleshooting.md`。

---

## 6. 交付前自检清单（逐条确认）

**语法与运行时**
- [ ] 没有 Lua 5.3+ 语法（`//`、`&`、`|`、按位 `~`、`<<`、`>>`）和不存在的函数（`collectgarbage`、`os.execute`、`os.exit`、`os.getenv`、`io.popen`、`math.type`）。
- [ ] 代码块配对完整；不等于是 `~=`；字符串拼接是 `..`；变量与函数都用 `local`，使用前已定义。

**API 与外设**
- [ ] CC API 用 `.` 调用；每个函数都能在第 4 节、`api-reference.md` 或 `peripherals.md` 中找到。
- [ ] 模组外设的方法来自用户游戏里的 `getMethods` 或 `mod-*.md` 的实测记录（并说明了版本），没有凭记忆编造；没有把模组行为写成 CC 本体的行为。
- [ ] 外设名字真实可用；`wrap`/`find` 检查了 `nil`；`list()`/`tanks()` 用 `pairs`；`pushItems` 传名字字符串。
- [ ] 海龟：检查了燃料（含 `"unlimited"`）、每个移动/挖掘的返回值、沙砾、背包满。

**结构与事件**
- [ ] 所有无限循环里都有会 yield 的调用；需要同时等多种事件时没有用 `sleep`。
- [ ] 计时器事件比对了 ID；`os.pullEventRaw` 处理了 `terminate`。
- [ ] 等待聊天/触摸/按键的代码里没有调用会等待的外设方法；需要时用 `parallel` 分开。
- [ ] 自启的程序没有覆盖用户已有的 `startup.lua`；需要续跑的保存了进度。

**交付内容**
- [ ] 需求不明确时先对齐了目标；选的是最简单的可行方案；没要求的功能列在"可选增强"。
- [ ] 附了安装清单、运行步骤、关键设计决策与验证方法；说明了版本依赖（第 4.4 节）、服务器配置依赖、区块加载要求。
- [ ] 屏幕上的文字是英文/拼音；用到中文的地方按 `chinese-text.md` 选了经过验证的途径并说明了前提。
- [ ] 安全认证代码只在用户同意后加入；借鉴的教程/旧代码已逐个函数核对。
- [ ] 有 cct-run 时：交付前已运行，写明了结果和没覆盖的部分；没有时：没有写“已测试”，并在第一次交付时提醒过可以安装测试环境。

**长期运行 / 大型程序（用户同意采用这种规模时）**
- [ ] 网络请求有超时和有限次数的重试；外设调用用 `pcall` 防止中途断开，处理 `peripheral`/`peripheral_detach`。
- [ ] 设置/状态文件读取失败时回退默认值；改过的调色板、红石输出在退出时恢复；日志不写入密码、token。
