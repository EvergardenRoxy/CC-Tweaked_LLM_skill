---
name: minecraft-cc-tweaked
description: 协助用户为 Minecraft 模组 CC：Tweaked（ComputerCraft，CC:T，CraftOS）编写、审查、调试 Lua 程序：计算机、海龟（turtle）、口袋计算机、命令计算机，以及显示器、调制解调器、箱子/储罐/能量方块、扬声器、打印机、磁盘驱动器、红石继电器等外设；rednet/GPS 网络、红石控制、HTTP/WebSocket。当用户提到 CC: Tweaked、ComputerCraft、CC:T、CraftOS、海龟/turtle、rednet、peripheral.wrap/find、startup.lua、monitor 显示器、有线调制解调器、pastebin/wget，或要求用 Lua 在 Minecraft 里自动化挖矿、种植、仓储、监控、远程控制时使用。
---

# Minecraft CC: Tweaked（ComputerCraft）编程协助指南

本 Skill 是编写 CC: Tweaked 程序时的**权威参考**，内容以官方文档 <https://tweaked.cc> 为准。CC: Tweaked 的 Lua 环境与普通 Lua 有不少差别（Lua 5.2 运行时、事件驱动、外设命名、海龟燃料……），网上还有大量旧版 ComputerCraft（1.7.10 时代）的过时写法。**你记忆里的 CC 写法可能是错的或过时的，必须以本 Skill 和 tweaked.cc 为准。**

本文件是常驻的核心部分（规则、执行模型、API 速查、自检清单）。细节放在 `references/` 中，按第 1 节的索引**按需读取**。

**本 Skill 的用法：先拆解、先对齐，再写码。** 收到请求后先拆解问题、想出最简单可行的方案，和用户确认目标（第 2.0 节），再按 2.2 节从约束推导结构与失败处理。不要一上来就交付一份复杂、难维护、还不一定符合用户需求的程序。`templates.md` 里的程序只是某组约束下的一个答案，用来核对写法，**不要把模板改改名字就交付**。

---

## 0. 给 AI 的铁律（先读这一节）

0. **先拆解问题、先给最简单的方案、先和用户对齐目标，再写复杂代码**（第 2.0 节）。能用现成程序（`excavate`、`tunnel`、`go`）、原版红石/漏斗或二十行脚本解决的，就不要写带界面、配置系统和网络协议的大程序。用户没要求的功能（图形界面、日志、配置文件、重试框架、认证）只作为"可选增强"列出，不要直接塞进代码。
1. **运行时是 Lua 5.2（Cobalt），不是 5.1/LuaJIT/5.3/5.4。** 没有整数子类型、没有 `//` 和位运算符 `& | ~ << >>`（用 `bit32.band` 等）、没有 `collectgarbage`、`os.execute`、`os.exit`、`os.getenv`、`io.popen`。`goto`、`table.unpack`、`table.pack`、`utf8`、`string.pack` 可用。详见第 4.1 节。
2. **只使用 tweaked.cc 上存在的 API。** 不确定某函数是否存在、参数顺序、返回值时，先查 `references/api-reference.md`；仍不确定，让用户在游戏里用 `lua` 交互环境执行 `peripheral.getMethods("名字")`、`help 主题` 验证，**不要编造函数**。
3. **CC 的 API 一律用 `.` 调用**：`turtle.forward()`、`peripheral.wrap("top")`、`chest.list()`、`mon.write("x")`、`fs` 文件句柄 `h.readAll()`。只有 `io` 文件句柄（`f:read("l")`）和 `vector` 对象（`v:length()`）用 `:`。
4. **外设名字只有两种**：相邻方块用方向 `"top" "bottom" "left" "right" "front" "back"`（相对计算机朝向）；经有线调制解调器连接的用网络名，如 `"minecraft:chest_0"`（右键调制解调器时聊天栏显示）。不要编造名字；优先 `peripheral.find("类型")`，并且**检查返回 nil** 后用 `error("…", 0)` 给出清楚提示。
5. **会失败的操作要检查返回值。** 海龟动作失败时**不抛错**，而是返回 `false, "原因"`；`fs.open`、`http.get`、`peripheral.wrap`、`rednet.receive(超时)` 失败返回 `nil`。不检查就会在后面出现 `attempt to index a nil value`。
6. **长时间运行的循环必须让出（yield）。** `while true do` 里必须有 `os.pullEvent`/`sleep`/海龟动作/外设调用等会 yield 的操作，否则报 `Too long without yielding`，程序被强制终止。
7. **`sleep()` 会丢弃等待期间到来的所有其他事件。** 既要定时又要响应事件（按键、rednet、显示器触摸），用 `os.startTimer` + `os.pullEvent` 事件循环，或 `parallel.waitForAny`（见第 3 节）。
8. **`inventory.list()`、`fluid_storage.tanks()` 返回稀疏表**：空槽是 `nil`，必须用 `pairs`，不能用 `ipairs` 或 `#`。槽位从 **1** 开始。
9. **`pushItems`/`pullItems`/`pushFluid`/`pullFluid` 的第一个参数是对方外设的名字字符串**（`peripheral.getName(x)`），不是 wrap 出来的表；两个容器要在**同一个有线网络**上。海龟自己的物品栏不是 `inventory` 外设，从箱子取放物品用 `turtle.suck*`/`turtle.drop*`。
10. **海龟移动消耗燃料**（转向不耗）。程序开头检查 `turtle.getFuelLevel()`（可能返回字符串 `"unlimited"`）；挖掘程序要处理沙砾/沙子掉落、生物挡路、背包满、返回路径的燃料。
11. **计算机所在区块卸载时会关机，所有变量丢失。** 需要开机/重进世界后自动运行，写 `startup.lua`；需要断点续跑，把进度写进文件（`settings` 或 `fs`）。
12. **版本不确定时先问版本**（CC: Tweaked 版本号形如 `1.113.1`，可在游戏里 `print(_HOST)` 查看）。版本敏感特性见第 4.9 节。
13. **给出的程序必须附"安装清单"**：需要什么设备（普通/高级计算机、海龟及其工具）、外设摆在哪一面或网络名、文件保存路径、如何运行；交付前逐条过第 6 节自检清单。
14. **默认用户没有中文字体环境，不生成显示中文的代码。** CC 的终端和显示器只有自带的 256 个字符，中文显示为乱码。界面文字（包括 `print`/`error`/`printError` 的提示和报错信息）一律用英文或拼音并告诉用户原因；代码注释可以用中文；`#字符串` 是字节数。用户明确想要中文界面时，提示可用社区点阵字体库 [utf8display](https://git.liulikeji.cn/xingluo/ComputerCraft-Utf8/src/branch/main/utf8display)，说明前提并经用户确认后再写，见 `app-engineering.md`。
15. **只有在用户确实需要并同意时，才把程序写成大型工程**（长期运行、联网、带界面）：那时按 `references/app-engineering.md` 的规范来——模块化、全部 `local`、HTTP 有超时和重试、设置有默认值与校验、外设调用防断开、退出时恢复调色板。
16. **不照搬模板、教程或记忆中的代码。** 网上教程和旧代码常含不存在的函数（如 `textutils.sha256`）、错误的环境假设（如 `os.run` 里调用 `shell`）和无效的安全措施；逐个函数核对，按 `references/design-thinking.md` 第六节评审后再采用。
17. **重视安全，但安全认证代码只在用户同意后才加入。** Minecraft 服务器大多是熟人或受管理的环境，普通自动化程序不需要密码、加密和认证。默认做法：在风险提示里用一两句话说明风险（如"rednet 消息别人也能发"），并提出可选的防护方案，**等用户确认需要再写**。用户明确要求门禁、密码、权限、远程认证时，先和用户确认威胁模型（防谁、对方能接触到什么），再按 `references/security.md` 选机制，并说明代码防不住的部分（拆机、OP）。无论是否加认证，都不要写出执行收到的消息内容（`load` 网络数据）这类危险代码。
18. **本文件没写到的细节，先读对应的 `references/` 文件再回答**（见第 1 节）。

---

## 1. 参考文件索引（按需读取）

| 遇到这种情况 | 必须先读 |
|---|---|
| 要用第 4 节没列出的函数，或需要确切的参数/返回值（`fs`、`term`、`textutils`、`settings`、`http`、`os`、`colors`、`window`、`cc.*` 库……） | `references/api-reference.md` |
| 要操作外设：箱子/储罐/能量方块、显示器、扬声器、打印机、磁盘驱动器、红石继电器、命令方块；有线网络命名；物品/方块详情表的字段 | `references/peripherals.md` |
| 写海龟程序：挖矿、隧道、砍树、种田、建造、合成、装备工具、坐标与朝向跟踪 | `references/turtle.md` |
| 计算机间通信（rednet/modem）、GPS 搭建与定位、HTTP/WebSocket、下载程序 | `references/networking.md` |
| 事件循环、定时器、`parallel`、协程、按键/鼠标/显示器触摸、`terminate` 处理 | `references/events-and-concurrency.md` |
| 要写一个新程序，想找相似案例（仓储统计、自动熔炉、伐木、隧道、远程控制、触摸按钮、能量监控、音乐……） | `references/templates.md` |
| 用户贴出报错原文，或说"不工作/没反应/卡住/报错" | `references/troubleshooting.md` |
| 问到服务器配置（HTTP 白名单、磁盘空间、燃料开关）、`/computercraft` 命令、版本差异、Lua 兼容性 | `references/config-and-versions.md` |
| 写几百行以上的应用：多模块结构、并发/可靠 HTTP（重试、超时、大文件）、安装器/更新器、设置持久化、外设选择与热插拔、日志、调色板、中文显示、发布 | `references/app-engineering.md` |
| **任何新需求的设计阶段**：怎么从需求推导结构、CC 的硬约束、失败模式分析、思路模式库（单一等待点、真实时间节拍、有界缓冲、执行后验证、数据驱动规则、状态对账、自检、协议设计……）、评审别人代码的方法 | `references/design-thinking.md` |
| 密码、登录终端、门禁、权限、加密、远程认证、"防止别人改我的程序" | `references/security.md` |
| 新手问题：在哪里输入代码、`No such program`、怎么读文档签名、外部编辑器/文件位置、模拟器、中文资料的可信度 | `references/getting-started.md` |

---

## 2. 协助流程

### 2.0 先拆解、先对齐目标（收到请求后的第一步）

1. **复述目标**：用一句话说出你理解的用户想达成什么（结果，而不是用户提到的手段）。用户说"写个程序把矿石搬到熔炉"，真正的目标可能是"矿石自动变成锭"。
2. **拆解**：把请求拆成几个子问题（输入从哪来、要做什么、输出到哪、多久一次、出错怎么办）。
3. **从简单到复杂列方案**，优先考虑：
   - 不写代码：原版漏斗/红石、其他已装模组的功能、ROM 自带程序（`excavate`、`tunnel`、`go`、`refuel`）；
   - 几十行的单文件脚本；
   - 最后才是多文件、带界面/配置/网络协议的系统。
4. **推荐一个能满足目标的最简单方案**，说明它的局限，以及以后要扩展时往哪走。
5. **只问会改变方案的问题**，合并成一条消息，并给出默认假设（"如果没有特别要求，我按 X 来写"）。
6. **用户确认后再写代码**。

什么时候可以跳过协商、直接给答案：请求小而明确（"海龟怎么前进 10 格""这段报错什么意思"）、改动范围清楚的修 bug、用户已经给出完整需求并要求直接写。即使跳过，也要在回答开头写明你的假设。

**复杂度预算**：交付的代码只包含达成目标所需的部分。日志、配置文件、图形界面、重试框架、认证、多语言等，用户没要求就放进"可选增强"一栏，让用户挑选。

### 2.1 先问清的信息（缺失才问，已知就不要再问）

| 要确认的信息 | 为什么重要 |
|---|---|
| CC: Tweaked 版本、Minecraft 版本、加载器（Forge/NeoForge/Fabric） | 部分 API 随版本增加；旧版 ComputerCraft（MC 1.7.10/1.12）差别很大 |
| 设备类型：普通/高级计算机、普通/高级海龟、口袋计算机、命令计算机 | 颜色、鼠标事件、燃料上限、`commands` API 只在特定设备上可用 |
| 外设及连接方式：贴在计算机哪一面，还是通过有线调制解调器联网 | 决定外设名字和能否用 `pushItems` 跨容器搬运 |
| 涉及的模组方块（Mekanism、热力、AE2、Create……） | 外设类型名、是否提供 `inventory`/`fluid_storage`/`energy_storage` 之外的专有方法 |
| 是否要开机自启、是否要在区块卸载后继续 | 决定 `startup.lua` 与进度持久化 |
| 是否是多人服务器、HTTP 是否开放 | `http`/`wget`/`pastebin` 可能被服务器禁用或白名单限制 |
| 是否需要防止他人操作（仅在涉及门禁、远程控制、贵重物品时提一句） | 默认不加认证；用户需要时才按 `security.md` 设计 |
| 现有代码、报错原文（含文件名和行号） | 排错必需 |

### 2.2 设计步骤（详见 `references/design-thinking.md`）

1. **翻译成 CC 原语**：输入来自哪里（事件、轮询外设、红石、网络、计时器），输出到哪里，哪些状态要持久化。
2. **列约束**：时间粒度、TPS、外设调用耗时、事件丢失、区块加载、外设变化、网络不可靠、磁盘/内存、字符集、谁能接触机器——逐条判断是否影响本需求。
3. **选结构**：一次性脚本 / 轮询循环 / 单一事件循环 / `parallel` 多任务 / 状态机 / 多台计算机，并说出理由。
4. **失败模式**：对每个外部交互问"失败、不返回、对象消失、重复乱序、做了没生效"怎么办，决定检查、超时、重试、降级。
5. **可观测性与验证**：启动自检、状态显示/计数器/日志；规划用户一步步验证的方法（先在 `lua` 里试单个调用）。
6. 写代码（配置放顶部 `local` 常量；可能失败的调用检查返回值；循环里有 yield），过第 6 节自检清单，按 2.3 交付。

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

【怎么装、怎么跑】
1. 放好设备与外设；有线调制解调器要右键使其变红（已连接）。
2. 在计算机里 `edit startup.lua`，粘贴代码（Ctrl 打开菜单保存）；
   或在开启 HTTP 的环境用 `wget <url> startup.lua` / `pastebin get <代码> startup.lua`。
3. 运行 `startup` 或 `reboot`；Ctrl+T 终止程序，Ctrl+R 重启，Ctrl+S 关机（均需长按）。

【怎么验证】先在 `lua` 里验证哪几个调用；运行后看到什么说明正常。

【风险提示】燃料/区块加载/外设名字/服务器配置/性能……；如有安全风险，用一两句话说明。

【可选增强】（用户没要求、所以没写进代码的功能，例如：显示器界面、配置文件、日志、断点续跑、访问认证——需要哪个告诉我）
````

---

## 3. 核心概念与执行模型

- **计算机**：开机运行 CraftOS（`bios.lua` → `shell`），然后执行启动文件（`startup.lua` 或 `startup/` 目录下的全部文件，按文件名字典序），再进入命令行。普通计算机只有灰度，**高级**计算机有 16 色和鼠标事件。
- **海龟**：带 16 格物品栏、可移动的计算机，左右各一个升级槽（钻石镐/斧/剑/锄/铲、无线/末影调制解调器、扬声器、工作台）。
- **口袋计算机**：手持计算机，有 `pocket` API；可装一个升级（如无线调制解调器）。
- **命令计算机**：只能创造模式获取，有 `commands` API 可执行原版命令。
- **文件系统**：每台计算机有独立硬盘（默认约 1 MB，服务器可配），`/rom` 只读，软盘挂载在 `/disk` 等目录（以 `disk.getMountPath(名字)` 为准）。

**执行模型**（最重要）：

```text
每台计算机 = 一个 Lua 程序在协程里运行，靠"事件"驱动：
  os.pullEvent(过滤)   → 让出（yield），直到队列里出现匹配的事件才继续
  sleep(n)            → 内部 = startTimer + 只等这个 timer 事件；等待期间其他事件被丢弃
  外设方法/海龟动作     → 内部也会让出，等服务器在游戏刻里执行完再返回（通常 ≥ 1 刻 = 0.05 秒）
  事件队列最多 256 个；溢出的事件被丢弃
  长时间不让出         → "Too long without yielding"，程序被终止
```

- 程序**不会**并行执行；`parallel.waitForAny/All` 是在多个协程间切换：一个协程让出时另一个才运行。
- 时间单位是**秒**，精度 0.05 秒（1 游戏刻），`sleep(0.01)` 实际等 0.05 秒。
- 典型结构选择：

| 需求 | 写法 |
|---|---|
| 每 N 秒做一次，不需要响应输入 | `while true do 工作() sleep(N) end` |
| 等某种事件（触摸、消息、红石变化） | `while true do local e, a, b = os.pullEvent("monitor_touch") … end` |
| 定时 + 响应事件 | `os.startTimer` 事件循环，或 `parallel.waitForAny(定时循环, 事件循环)` |
| 批量调用外设方法提速 | 把调用包成函数列表交给 `parallel.waitForAll`（一次别塞几百个） |

计时器事件循环模板：

```lua
local INTERVAL = 5
local timer = os.startTimer(INTERVAL)
while true do
    local event, p1, p2, p3 = os.pullEvent()
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

> 本节覆盖日常写程序所需的核心 API。表里没有的函数，先查 `references/api-reference.md`。

### 4.1 Lua 5.2（Cobalt）与 CraftOS 的差别

| 写法 | 在 CC: Tweaked 中 |
|---|---|
| `a // b`、`a & b`、`a << 2`、`~a` | **语法错误**。用 `math.floor(a / b)`、`bit32.band(a, b)`、`bit32.lshift(a, 2)`、`bit32.bnot(a)` |
| `math.type`、`math.tointeger`、`math.maxinteger` | 不存在（没有整数子类型，数字都是浮点） |
| `string.format("%d", x)` | `x` 是小数时行为依实现而定；先 `math.floor(x)`，或用 `%.1f` |
| `collectgarbage`、`os.execute`、`os.exit`、`os.getenv`、`os.remove`、`io.popen` | 不存在。删文件用 `fs.delete`，退出程序用 `return` 或 `error("…", 0)` |
| `goto continue` / `::continue::` | 可用 |
| `table.unpack`、`table.pack`、`select("#", …)`、`load(str, name, "t", env)` | 可用（`unpack`、`loadstring` 作为旧别名仍存在，但优先用新名） |
| `setfenv`/`getfenv` | 仅部分可用，不要依赖；用 `load` 的 `env` 参数 |
| `require("mod")` | 可用；按 `?.lua`、`?/init.lua`、`/rom/modules/main/?.lua` 搜索，**相对当前程序目录**；子目录写 `require("a.b")`，不要写 `require("a/b.lua")` |
| `os.loadAPI` | 已弃用，用 `require` |
| `...` | 程序的命令行参数：`local a, b = ...`；旧的全局 `arg` 只在 shell 启动的程序中存在 |

### 4.2 外设基础

```lua
local mon = peripheral.find("monitor")                  -- 任意一个显示器
local chest = peripheral.wrap("minecraft:chest_0")      -- 按名字
if not chest then error("minecraft:chest_0 not found; is the wired modem enabled?", 0) end
local drives = { peripheral.find("drive") }             -- 全部驱动器（返回多个值，用表接住）
print(peripheral.getName(chest), peripheral.getType(chest))
for _, name in ipairs(peripheral.getNames()) do print(name, peripheral.getType(name)) end
```

| 函数 | 说明 |
|---|---|
| `peripheral.getNames()` | 所有可用外设名（方向 + 网络名） |
| `peripheral.isPresent(name)` / `getType(name或对象)` / `hasType(x, type)` | 是否存在 / 类型（可能多个，如 `"minecraft:chest"` 和 `"inventory"`）/ 是否某类型 |
| `peripheral.getMethods(name)` | 方法名列表——**不确定外设有什么方法时让用户跑这个** |
| `peripheral.wrap(name)` | 返回方法表，不存在返回 `nil` |
| `peripheral.find(type [, filter])` | 返回**所有**匹配外设（多返回值）；`filter(name, wrapped)` 返回 true 才保留 |
| `peripheral.call(name, method, ...)` | 不 wrap 直接调用 |
| `peripheral.getName(wrapped)` | wrap 对象 → 名字（`pushItems` 需要它） |

有线网络：计算机和每个外设各贴一个**有线调制解调器**，用**网线**连起来，**右键调制解调器**使其连接（变红并在聊天栏显示名字）。外设接入/断开时触发 `peripheral` / `peripheral_detach` 事件。细节见 `references/peripherals.md`。

### 4.3 物品栏 / 流体 / 能量（通用外设，1.94.0+）

| 方法（`inventory`） | 说明 |
|---|---|
| `size()` | 槽位数 |
| `list()` | `{[槽]={name=, count=, nbt=?}}` 稀疏表 |
| `getItemDetail(slot)` | 详细信息（`displayName`、`maxCount`、`tags`、`damage`、`enchantments`…），空槽 `nil` |
| `getItemLimit(slot)` | 该槽最大数量（1.96.0+） |
| `pushItems(toName, fromSlot [, limit [, toSlot]])` | 推到另一个容器，返回实际数量 |
| `pullItems(fromName, fromSlot [, limit [, toSlot]])` | 从另一个容器拉，返回实际数量 |

| 方法（`fluid_storage` / `energy_storage`） | 说明 |
|---|---|
| `tanks()` | `{[i]={name=, amount=}}` 稀疏表，单位 mB |
| `pushFluid(toName [, limit [, fluidName]])` / `pullFluid(fromName [, limit [, fluidName]])` | 返回移动量 |
| `getEnergy()` / `getEnergyCapacity()` | FE；无法测量吞吐量 |

```lua
-- 把输入箱里所有圆石推到输出箱
local input = peripheral.wrap("minecraft:chest_0")
local output = peripheral.wrap("minecraft:chest_1")
local outName = peripheral.getName(output)
for slot, item in pairs(input.list()) do
    if item.name == "minecraft:cobblestone" then
        input.pushItems(outName, slot)
    end
end
```

### 4.4 海龟要点（详见 `references/turtle.md`）

| 类别 | 函数（`Up`/`Down` 变体同理） | 返回 |
|---|---|---|
| 移动 | `forward() back() up() down()` | `ok, 原因`；耗 1 燃料 |
| 转向 | `turnLeft() turnRight()` | `ok, 原因`；不耗燃料 |
| 挖/放/攻击 | `dig([side]) place([文本]) attack([side])` | `ok, 原因` |
| 探测 | `detect()`、`inspect()`、`compare()` | `bool`；`inspect` 返回 `has_block, 数据表或原因` |
| 物品栏 | `select(slot)`、`getSelectedSlot()`、`getItemCount([slot])`、`getItemSpace([slot])`、`getItemDetail([slot [, detailed]])`、`transferTo(slot [, n])`、`compareTo(slot)` | 槽位 1–16 |
| 容器交互 | `drop([n])`、`suck([n])` | `ok, 原因`；前方没有容器时 drop 会把物品丢到地上 |
| 燃料 | `getFuelLevel()`、`getFuelLimit()`、`refuel([n])`（`refuel(0)` 检查是否可作燃料） | 数字或 `"unlimited"` |
| 装备/合成 | `equipLeft()`、`equipRight()`、`getEquippedLeft/Right()`（1.116.0+）、`craft([limit])`（需工作台升级） | |

- 普通海龟燃料上限 20,000，高级 100,000；一块煤 = 80 燃料。
- 用 `assert(turtle.forward())` 或自己的重试函数处理失败；沙砾会在挖掉后落下，要 `while turtle.detect() do turtle.dig() end`。

### 4.5 红石

```lua
redstone.setOutput("back", true)                 -- 15 级
redstone.setAnalogOutput("top", 7)                -- 0–15
local on = redstone.getInput("left")              -- bool
local level = redstone.getAnalogInput("right")    -- 0–15
os.pullEvent("redstone")                           -- 任意输入变化时触发（无参数）
```

- `rs` 是 `redstone` 的别名；面名同外设方向；捆绑线缆用 `getBundledInput`/`setBundledOutput` + `colors.combine`/`colors.test`。
- 一台计算机控制多处红石：用**红石继电器**（`redstone_relay`，1.114.0+）经有线网络连接，方法与 `redstone` API 相同。

### 4.6 网络（详见 `references/networking.md`）

```lua
peripheral.find("modem", rednet.open)              -- 打开所有调制解调器上的 rednet
rednet.send(5, { cmd = "start" }, "factory")        -- 发给 ID 5，协议 "factory"
local id, msg = rednet.receive("factory", 10)       -- 10 秒超时，超时返回 nil
rednet.broadcast("hello", "chat")
rednet.host("factory", "furnace1")                  -- 注册服务名
local server = rednet.lookup("factory", "furnace1") -- 查 ID，找不到返回 nil
```

- 消息可以是数字、字符串、布尔、表（不能含函数）。rednet **不加密**，多人服务器上别信任消息来源。
- 无线调制解调器范围 64 格（高处更远）；末影调制解调器无距离限制、可跨维度；有线调制解调器只在网线网络内。
- `gps.locate([timeout])` 需要已搭好的 4 台 GPS 主机，失败返回 `nil`。
- `http.get(url)` 返回响应句柄（`h.readAll()`、`h.getResponseCode()`、`h.close()`）或 `nil, 错误`；服务器可能禁用 HTTP 或屏蔽局域网地址。

### 4.7 终端与显示器

```lua
local mon = peripheral.find("monitor") or error("No monitor attached", 0)
mon.setTextScale(0.5)                     -- 0.5–5，步长 0.5；越小分辨率越高
mon.setBackgroundColour(colours.black)
mon.clear()
mon.setCursorPos(1, 1)
mon.setTextColour(colours.lime)
mon.write("Hello")                        -- write 不换行、不自动折行
local w, h = mon.getSize()
local old = term.redirect(mon)            -- 之后 print 输出到显示器
print("via print")
term.redirect(old)
```

- 坐标从 **(1,1)** 开始；`print`/`write` 会折行，`term.write`/`mon.write` 不会。
- 颜色常量 `colors.white … colors.black`（值为 1, 2, 4 … 32768）；`term.blit(文本, 前景, 背景)` 用 `0-9a-f` 字符串。
- 只有**高级显示器**能触摸：事件 `monitor_touch, 名字, x, y`；只有高级计算机有 `mouse_click`。
- 显示器尺寸变化触发 `monitor_resize`；复杂界面用 `window.create` 做缓冲防闪烁。

### 4.8 文件、设置与启动

```lua
local h = fs.open("/data/state.txt", "w")      -- 模式 r w a（1.109.0+ 还有 r+ w+），加 b 为二进制
h.write(textutils.serialise({ x = 1, y = 2 }))
h.close()

local f = fs.open("/data/state.txt", "r")
if f then
    local state = textutils.unserialise(f.readAll())
    f.close()
    print(state.x)
end

settings.define("mine.depth", { description = "Mining depth", default = 32, type = "number" })
local depth = settings.get("mine.depth")
settings.set("mine.depth", 64)
settings.save()                                  -- 写到 /.settings
```

- `fs` 的路径都是**绝对路径**，不考虑当前目录；`fs.combine(a, b)` 拼接路径。
- `textutils.serialise`/`unserialise`（Lua 表 ↔ 字符串），`serialiseJSON`/`unserialiseJSON`（JSON）。英美拼写两个版本都存在。
- 启动顺序：`/rom/autorun` → 磁盘上的 `startup(.lua)` 或 `startup/`（需 `shell.allow_disk_startup`）→ 根目录 `startup.lua` 或 `startup/*`。
- `shell.run("程序", "参数")` 运行其他程序；`os.reboot()`、`os.shutdown()`、`os.getComputerID()`、`os.setComputerLabel("名字")`（给计算机起名，挖下来后物品显示该名字）。

### 4.9 版本敏感特性（用到前确认版本）

| 特性 | 版本 |
|---|---|
| 通用外设 `inventory`/`fluid_storage`/`energy_storage` | 1.94.0+ |
| 外设多类型、`peripheral.hasType` | 1.99+ |
| `speaker.playAudio`、`cc.audio.dfpwm` | 1.100+ |
| Lua 5.2 运行时（移除 `arg` 伪参数等）、`fs.open` 的 `r+`/`w+` | 1.109.0+ |
| `cc.strings.split` | 1.112.0+ |
| 红石继电器 `redstone_relay` | 1.114.0+ |
| `turtle.getEquippedLeft/Right` | 1.116.0+ |
| `rednet.lookup` 的超时参数、`commands.getEntities` | 1.118.0+ |
| `cc.base64`、`commands.getDimension` | 1.119.0+ |
| `parallel.waitForAll` 的 `spawn` 参数 | 1.120.0+ |
| `turtle_storage`（海龟装备潜影盒等存储物品） | 1.121.0+ |

完整列表见 `references/config-and-versions.md`。

---

## 5. 最常见的错误

| 错误写法 | 后果 | 正确写法 |
|---|---|---|
| `turtle:forward()`、`mon:write("x")` | `bad argument` 报错 | `turtle.forward()`、`mon.write("x")` |
| `local chest = peripheral.wrap("chest")` | 返回 `nil`，后面 `attempt to index` | 用真实名字 `"left"`/`"minecraft:chest_0"`，或 `peripheral.find("inventory")` |
| `for i, item in ipairs(chest.list())` | 遇到第一个空槽就停止 | `for slot, item in pairs(chest.list())` |
| `chest.pushItems(other, slot)`（`other` 是 wrap 对象） | 报错 | `chest.pushItems(peripheral.getName(other), slot)` |
| `while true do if rs.getInput("top") then … end end` | `Too long without yielding` | 循环里加 `os.pullEvent("redstone")` 或 `sleep(…)` |
| `sleep(5)` 期间等 rednet 消息 | 消息被丢弃 | `rednet.receive(协议, 超时)` 或 `parallel` |
| `turtle.forward()` 不检查返回 | 撞墙/没燃料后坐标错乱 | `if not turtle.forward() then … end` 或 `assert(...)` |
| `turtle.dig(); turtle.forward()` 挖沙砾 | 沙砾落下，前进失败 | `while turtle.detect() do turtle.dig() end` |
| `if turtle.getFuelLevel() < 100` | 燃料无限时比较字符串报错 | 先判断 `== "unlimited"` |
| `math.floor(x / 2)` 写成 `x // 2` | 语法错误 | `math.floor(x / 2)` |
| `os.pullEvent("monitor_touch")` 用普通显示器 | 永远等不到 | 用高级显示器 |
| `startup.lua` 有 bug 或死循环 | 每次开机都崩/卡住 | 先手动运行测试；卡住时长按 Ctrl+T 终止再 `edit startup.lua`；若 Ctrl+T 无效（程序用了 `pullEventRaw`），在相邻磁盘驱动器放一张带空 `startup.lua` 的软盘再重启——磁盘启动文件优先 |

更多见 `references/troubleshooting.md`。

---

## 6. 交付前自检清单（逐条确认）

**语法与运行时**
- [ ] 没有 Lua 5.3+ 语法：`//`、`&`、`|`、`~`（按位）、`<<`、`>>`、整数除法。
- [ ] 没有不存在的函数：`collectgarbage`、`os.execute`、`os.exit`、`os.getenv`、`io.popen`、`math.type`。
- [ ] 每个 `function`/`if`/`for`/`while`/`do` 都有 `end`；`repeat` 配 `until`；不等于是 `~=`（不是 `!=`）；字符串拼接是 `..`。
- [ ] 全部变量与函数都用 `local`（除非确实要全局）；函数在使用前定义。

**API**
- [ ] 所有 CC API 用 `.` 调用；只有 `io` 句柄和 `vector` 用 `:`。
- [ ] 每个函数名都能在第 4 节或 `api-reference.md`/`peripherals.md` 中找到；没有编造的方法。
- [ ] 外设名字真实可用；`wrap`/`find` 结果检查了 `nil` 并给出清楚报错。
- [ ] `list()`/`tanks()` 用 `pairs`；`pushItems` 等传的是名字字符串；源和目标在同一有线网络。
- [ ] 海龟：检查了燃料（含 `"unlimited"`）、每个移动/挖掘的返回值、沙砾、背包满、选中的槽位。

**结构与事件**
- [ ] 所有无限循环里都有会 yield 的调用。
- [ ] 需要同时等待多种事件时没有用 `sleep`，而是事件循环或 `parallel`。
- [ ] 计时器事件比对了 ID（`p1 == timer`）；`os.pullEventRaw` 的分支处理了 `terminate`。
- [ ] 需要自启的程序给出了 `startup.lua`；需要续跑的保存了进度。

**交付内容**
- [ ] 附了安装清单（设备 → 位置/网络名 → 说明）和运行步骤。
- [ ] 写了关键设计决策与验证方法；程序结构是按本需求的约束推导的，不是模板换皮。
- [ ] 需求不明确时先拆解并与用户对齐了目标；选的是能满足目标的最简单方案。
- [ ] 没有加入用户未要求的功能（界面、配置系统、日志、认证……），它们列在"可选增强"里。
- [ ] 安全认证类代码只在用户同意后加入；未加入时在风险提示里简要说明了风险和可选方案。
- [ ] 借鉴的教程/旧代码已逐个函数核对；用户要求的安全功能写了威胁模型和局限。
- [ ] 说明了版本依赖（第 4.9 节）、服务器配置依赖（HTTP、燃料）、区块加载要求。
- [ ] 提醒用户出错时贴出完整报错（文件名:行号: 消息），排错按 `troubleshooting.md` 流程。

**长期运行 / 大型程序（用户同意采用这种规模时；读过 `app-engineering.md`）**
- [ ] 网络请求有超时、有限次数的重试，4xx 不盲目重试；并发请求 URL 互不相同；大响应分块读取。
- [ ] 外设调用用 `pcall` 防止中途断开；处理 `peripheral`/`peripheral_detach`。
- [ ] 设置/状态文件读取失败时回退默认值而不是崩溃；保存前检查空间。
- [ ] 改过的调色板、红石输出在退出时恢复；日志不写入密码、cookie、token。
- [ ] 界面文字和 `error`/`printError` 信息是英文/拼音；只有用户确认使用 utf8display 后，经它渲染的文字才用中文。
