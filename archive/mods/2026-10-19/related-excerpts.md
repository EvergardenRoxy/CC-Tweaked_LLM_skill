# 从通用指南移出的模组专用说明

归档日期：2026-10-19。原始上下文可按来源提交查询，不作为当前 API 保证。

## SKILL.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/SKILL.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
3: description: 协助用户为 Minecraft 模组 CC：Tweaked（ComputerCraft，CC:T，CraftOS）编写、审查、调试 Lua 程序：计算机、海龟（turtle）、口袋计算机、命令计算机，以及显示器、调制解调器、箱子/储罐/能量方块、扬声器、打印机、磁盘驱动器、红石继电器等外设，和 Create、Advanced Peripherals 等模组提供的外设；rednet/GPS 网络、红石控制、HTTP/WebSocket、显示器界面。当用户提到 CC: Tweaked、ComputerCraft、CC:T、CraftOS、海龟/turtle、rednet、peripheral.wrap/find、startup.lua、monitor 显示器、有线调制解调器、pastebin/wget，或要求用 Lua 在 Minecraft 里自动化挖矿、种植、仓储、监控、工厂控制、远程控制时使用。
20: 2. **只使用真实存在的 API，并分清 CC: Tweaked 本体和模组。** 本体 API 以 tweaked.cc 和 `api-reference.md` 为准；Create、Advanced Peripherals 等**模组**的外设方法各版本不同，以用户游戏里 `peripheral.getMethods("名字")` 的结果为准，本 Skill 的实测记录在 `mod-*.md`（标明了模组和版本）。不确定就让用户在 `lua` 里查，**不要编造函数**，也不要把模组的行为当成 CC 本体的行为。
31: 13. **CC 的终端和显示器不能显示中文。** 界面文字、`print`/`error` 信息一律用英文或拼音，并告诉用户原因；代码注释可以用中文。需要中文时（中文界面、聊天框收发中文、Create 显示板），先读 `chinese-text.md`：每条途径都有前提，有的只在特定模组上可用。
46: | **Create（机械动力）模组**的外设：应力表、转速表、转速控制器、显示链接器（显示板）、物品保险库；离合器等机械行为 | `references/mod-create.md` |
47: | **Advanced Peripherals 模组**的外设：聊天框、玩家探测器 | `references/mod-advanced-peripherals.md` |
48: | 任何**中文**：中文界面、聊天框收发中文、Create 显示板显示中文、字符串长度与编码、测试里注入中文 | `references/chinese-text.md` |
83: | 涉及的模组方块及**模组版本**（Create、Advanced Peripherals、Mekanism、AE2……） | 模组外设的类型名、方法和行为随模组和版本变化 |
```

## references/chinese-text.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/references/chinese-text.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
12: | Advanced Peripherals 聊天框发给玩家的消息 | 能 | `sendFormattedMessageToPlayer` + JSON 里的 `\uXXXX` 转义（`mod-advanced-peripherals.md`）；`sendMessageToPlayer` 发中文是乱码 | 模组 |
13: | Advanced Peripherals 聊天框收到的玩家消息 | 能 | 读 `chat` 事件的 `messageUtf8`（第 5 个参数）；普通的消息参数里中文是 `?` | 模组 |
14: | Create 显示链接器 → 显示板 | 能 | `writeBytes(字节表)`（`mod-create.md`）；`write("中文")` 是乱码 | 模组 |
22: - **从模组（Java）传进 Lua 的文字**：U+00FF 以上的字符（中文等）一律变成 `?`。需要原文时找模组另外提供的 UTF-8 字段（如聊天框的 `messageUtf8`）。
28: - fixture 里注入中文事件（如聊天框的 `messageUtf8`）：把每个 UTF-8 字节写成不超过 U+00FF 的转义，例如 `"å·¥"` 是“工”。直接写中文的话程序收到的是 `?`（和游戏里 Java 传来的文字一样）；新版 cct-run 会在摘要的 `notes` 里用 `fixture_text` 提醒。
45: 工厂里只是想让人看到中文状态时，Create 的显示板（`mod-create.md`）往往比 utf8display 简单：不需要下载字体，也不占电脑的硬盘。
```

## references/peripherals.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/references/peripherals.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
226: 模组方块（Mekanism、AE2、热力、Create、Advanced Peripherals……）可能提供 `inventory` 等通用方法之外的专有方法，名字和参数**各模组各版本都不同**。不要凭记忆写，按以下步骤：
239: - **先测清楚哪个外设真正起作用**：名字和玩家的描述不一定对应真正控制机器的那个外设。逐个改变设置，看读数和产量的变化，用数据确认后再写进程序（例子见 `mod-create.md`）。
245: | Create（机械动力） | `mod-create.md` | 应力表、转速表、转速控制器、显示链接器与显示板、物品保险库；离合器、应力与转速的关系 |
246: | Advanced Peripherals | `mod-advanced-peripherals.md` | 聊天框（事件参数、收发中文、冷却）、玩家探测器 |
```

## references/troubleshooting.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/references/troubleshooting.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
61: | 53 | 模组外设返回的中文、聊天框 `chat` 事件里的消息变成 `?` | 语义错 | U+00FF 以上的字符从 Java 进 Lua 时变成 `?`；聊天框用 `messageUtf8`（`{ os.pullEvent() }` 的 `ev[6]`，`chinese-text.md`、`mod-advanced-peripherals.md`） |
64: | 56 | 程序用聊天框发的中文、写到 Create 显示板的中文在游戏里是乱码 | 语义错 | Lua 字符串是字节，直接传给模组会逐字节变成字符。聊天框用 `sendFormattedMessageToPlayer` + JSON `\uXXXX` 转义，显示链接器用 `writeBytes(字节表)`（`chinese-text.md`） |
65: | 57 | Create 显示板停在旧内容上不更新 | 语义错 | 显示板是机械方块，要有转速才会更新；程序空闲时把整个传动网络设成 0 rpm 就会这样。只断开产线，保持主轴转动（`mod-create.md`） |
66: | 58 | 用红石控制 Create 离合器，开和停反了 | 语义错 | 离合器通红石时**断开**：输出红石 = 停止（`mod-create.md`） |
```

## references/events-and-concurrency.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/references/events-and-concurrency.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
172: 在 cct-run（运行的是 CC: Tweaked 1.120.2 本身的代码）里实测：同一个单循环程序每 0.5 秒读一次箱子和外设，同时收 20 条聊天指令，只处理了 11 条，而且计时器第一次触发后就丢了，轮询从此停止；改成下面的三协程结构，20 条全部处理。在真实游戏里的两次联合测试中，两个 AI 写的 Create 工厂控制程序都遇到了这两个现象。
218:         if ev[1] == "monitor_touch" or ev[1] == "chat" then
233:             elseif ev[1] == "chat" and ev[3] == "!stop" then
248: - 不要在监听协程里调用 `chest.list()`、`setTargetSpeed`、`sendMessageToPlayer` 这类方法；要调用就放进队列交给工作协程。
```

## references/app-engineering.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/references/app-engineering.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
414: - **中文显示**：CC 的终端和显示器不能显示中文；用户要中文界面时的选择（utf8display 点阵字体、Create 显示板、聊天框）和前提见 `chinese-text.md`。
```

## references/testing.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/references/testing.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
67:    - **模组外设**（Create、Advanced Peripherals 等）：如果 `cct_guide` 第 5 节有 `scripted` 外设（cct-run 新版本），用它描述：类型名，以及每个方法返回什么（`returns`、`sequence`、`error`，`sets` 让设置方法改变读取方法的返回值），时间线的 `method` 动作可以在某一刻改变返回值（比如让应力超过 95%）。数值要来自实机：`cct_live_peripheral`、`cct_live_trace` 里的 `peripheral_return`，或用户在 `lua` 里查到的结果；不要凭记忆编。它默认按会等待的方法处理，所以“外设调用期间丢事件”的问题在模拟器里也会出现。没有这个功能时，模组外设只能在实机上测；在测试程序里用 Lua 替身（覆盖 `peripheral.call`）也能跑通逻辑，但替身调用不会进 trace、不会等待，**测不出事件丢失**，测试结论里要写明。
68:    - **模组事件**（如聊天框的 `chat`）用时间线的 `event` 注入，参数顺序必须照搬实机记录里的真实事件。要注入 UTF-8 文字（如 `messageUtf8`），把每个字节写成不超过 U+00FF 的转义（`"\u00e5\u00b7\u00a5"` 是“工”）；直接写中文的话，程序收到的是 `?`（和游戏里 Java 传来的文字一样，新版本会在 `notes` 里用 `fixture_text` 提醒）。**不要为了好测给程序加一套英文指令**，那样真正的中文路径没测到（`chinese-text.md`）。
77: 5. **查原因要看记录，不要猜**：`cct_trace` 按 `kind` 筛选（`event`、`peripheral_call` / `peripheral_return`、`redstone_output`、`output`），或按 `ticks` 看某段时间；新版本还可以用 `contains` 按文字找（方法名、指令、屏幕上的字，如 `contains: "setTargetSpeed"`）；`cct_screen` 可以看某一刻的画面。读记录时注意：
```

## references/config-and-versions.md

[完整原文](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/blob/ac32d802605a9d115a3e1a4c15afaad32eeb887d/skills/minecraft-cc-tweaked/references/config-and-versions.md)，来源 `ac32d80`。下面保留原始行号与措辞，包括后续需要核对的旧结论。

```text
97: - 第三方附属模组（Advanced Peripherals、Plethora 等）提供的外设与方法不在 tweaked.cc 文档内，必须用 `peripheral.getMethods` 实测。
```
