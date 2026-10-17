# CC: Tweaked LLM Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI-Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](#ai-制作声明)

> 让 Claude（及其他 LLM）正确地编写、审查和调试 Minecraft **CC: Tweaked（ComputerCraft）** Lua 程序的 Agent Skill。

[CC: Tweaked](https://tweaked.cc) 是 ComputerCraft 的现代分支，为 Minecraft 加入可编程计算机、海龟（turtle）和各种外设，用 Lua 编程。它的运行环境与普通 Lua 差别不小：Lua 5.2（Cobalt）运行时、事件驱动、外设按方向或网络名访问、海龟要燃料……网上还有大量 1.7.10 时代的过时教程。LLM 凭记忆写出的 CC 程序经常调用不存在的函数、用错 `:` 和 `.`、在循环里忘记让出导致 `Too long without yielding`，或者用 Lua 5.3 的 `//` 直接语法错误。

本仓库提供一份**以官方文档 [tweaked.cc](https://tweaked.cc) 为准**的 Skill，把 CC: Tweaked 的执行模型、API、外设、海龟、网络、常见陷阱、程序模板和排错流程整理成 AI 可直接遵循的指南。

**设计理念：先拆解、先对齐，教思路而不是给答案。** 收到请求后，模型先拆解问题、从"不写代码 → ROM 自带程序 → 几十行脚本 → 完整系统"的阶梯里找最简单够用的方案，和用户确认目标后再写；用户没要求的功能（界面、日志、配置系统、认证）只作为"可选增强"列出。安全被视为重要话题，但认证/加密类代码**只在用户同意后**加入（Minecraft 服务器大多是可信环境），默认只在风险提示里简要说明风险和可选方案。

**教思路，而不是给答案。** 只塞给模型一堆成品程序，它只会生成相似的程序；换了设备、规模或网络条件就写错。因此本 Skill 的核心是**从需求推导程序的方法**：CC 世界的硬约束清单、程序结构的选择依据、对每个外部交互的失败模式分析、一组可组合的思路模式（看板 + 指令的三协程结构、按真实时间节拍、有界缓冲、执行后验证、数据驱动规则、状态对账、启动自检……），以及评审网上教程/旧代码的方法。模板只作为"某组约束下的参考答案"，并标注了"条件变了要换什么设计"。

[English summary](#english)

<a id="ai-制作声明"></a>

> [!IMPORTANT]
> **AI 制作声明：CC: Tweaked LLM Skill 采用生成式 AI 参与内容编写、代码校验与文档撰写。** AI 生成或修改的内容由项目维护者审阅、验证并承担最终维护责任。

> **当前版本 1.2.2**（2026-10），配套 [cct-run 0.2.2](https://github.com/EvergardenRoxy/CC-Tweaked_MCP)。这一版重新整理了结构：`SKILL.md` 从 455 行减到 328 行；Create 和 Advanced Peripherals 的实测记录独立成文件，和 CC: Tweaked 本体分开；新增中文（`chinese-text.md`）和显示器界面（`ui-design.md`）两篇说明；更正了聊天框发中文的写法，并写入联合测试 4 的结论（显示板显示中文、连发测试、不覆盖 `startup.lua` 等）。详见 [发行版说明](RELEASE_NOTES.md)。

---

## 能做什么

| 场景 | 示例提问 |
|---|---|
| 编写程序 | "用 CC 写一个仓库统计程序，把所有箱子的物品数量显示在显示器上" |
| 海龟自动化 | "写一个挖 3×3 隧道的海龟程序，背包满了自动回来卸货" |
| 网络与远程控制 | "用 rednet 做一个无线遥控器，远程开关基地的红石" |
| 模组机器与工厂控制 | "用 Create 的应力表和转速控制器做一个过载保护，在聊天栏下单生产" |
| 看板与触摸界面 | "做一个带侧边栏和按钮的显示器面板，能在屏幕上下单" |
| 审查程序 | "帮我看看这段 ComputerCraft 代码有没有问题" |
| 排查故障 | "报错 attempt to index a nil value / Too long without yielding 怎么办" |
| 测试与实机排错（需要 cct-run） | "写好之后先在模拟器里跑一遍再给我" / "接管 3 号电脑，看看这个安装脚本为什么装完打不开" |

每次回答都会给出：**整体思路 + 安装清单（设备 → 位置/网络名）+ 程序 + 运行步骤 + 风险提示**，并在交付前对照内置自检清单。

## Skill 内容

Skill 采用**渐进式加载**：触发时只加载精简的核心文件 `SKILL.md`（约 330 行：铁律、协助流程、执行模型、速查、自检清单），17 个细节文件由模型在需要时按索引读取。模组相关的内容放在单独的 `mod-*.md` 里，标明了实测的模组版本，不和 CC: Tweaked 本体混在一起。

**全部文件和各自的内容见 [Skill 内容一览](CONTENTS.md)。**

## 安装

本 Skill 遵循开放的 [Agent Skills](https://agentskills.io) 格式：把 `skills/minecraft-cc-tweaked/` 文件夹（**连同 `references/`**）放进 AI 工具的 skills 目录即可。Claude Code 可以直接从插件市场安装：

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

**Codex、Cursor、VS Code Copilot、Gemini CLI、Cherry Studio、Claude.ai，以及 ChatGPT / DeepSeek 等网页对话的安装方法，和 cct-run 的配置，见 [安装](INSTALL.md)。** 也可以从 [Releases](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases) 下载打包好的 `CCT_prompt_pack.zip`。

## 使用

安装后无需额外操作。当你提到 CC: Tweaked、ComputerCraft、CC:T、海龟/turtle、rednet、`peripheral.wrap`、`startup.lua`、显示器等内容时，Skill 会自动触发。

建议在提问时附上：

- **CC: Tweaked 版本**（游戏里 `print(_HOST)`）与 Minecraft 版本、加载器；用到模组外设时附上**模组和版本**
- 设备类型（普通/高级计算机、海龟、口袋计算机）、外设摆放位置或网络名（`peripherals` 程序可列出）
- 现有代码与完整报错（文件名:行号: 消息）

### 配套测试环境（可选）：cct-run

装上 [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) 并在 AI 客户端里配置它的 MCP 服务器（`cct-run mcp`）后，Skill 会让模型**在交付前先运行程序**：

- 在真实的 CC: Tweaked 1.120.2 代码上运行，不需要打开 Minecraft；
- 用 fixture 模拟箱子、显示器、红石等外设，模组外设用实机数值写成 `scripted`；
- 根据报错行号和事件记录修改，并在回答里如实写出测了什么、模拟没覆盖什么。

再装上 cct-live mod，模型还可以在你同意后接管游戏里的电脑，进行实机测试和排错：接管时聊天栏会提示，你可以随时用 `/cctlive detach <id>` 收回控制。

没有安装时，Skill 照常工作，只会在第一次交付程序时提醒一次可以安装。详见 [`references/testing.md`](skills/minecraft-cc-tweaked/references/testing.md)。

### 实测效果

cct-run 的联合测试 4（Create 订单产线：聊天下单、订单队列、过载保护、断电续跑）是 Skill 第一次参与的大型任务。和上一轮（同一个模型，联合测试 3 第 2 次）相比：

| | 联合测试 3 第 2 次 | 联合测试 4（Skill 1.2.0） |
|---|---|---|
| 任务时长 | 60 分钟 | 38 分钟 |
| 总 token | 7064 万 | 4382 万 |
| 卡在“外设调用期间丢事件”上的时间 | 约 34 分钟，交付的程序仍会丢指令 | 0：第一版就是 Skill 里的三协程结构 |
| 模组外设在模拟器里怎么测 | 自己写 Lua 替身 | cct-run 的 `scripted`，数值取自实机 |

两次的任务不同，只能粗略比较。测试暴露的问题（中文收发、显示器界面）已写进 1.2.2。图表和完整数据见 [cct-run 的 README](https://github.com/EvergardenRoxy/CC-Tweaked_MCP#ai-实测联合测试-3-与-4)。

## 准确性说明

- Skill 中全部 `lua` 代码块（目前 59 个）都用 [`scripts/validate_skill.py`](scripts/validate_skill.py) 通过 **Lua 5.2 编译器**（与 CC: Tweaked 的 Cobalt 运行时同版本）的语法检查，并把其中用到的全局 API 与 [tweaked.cc](https://tweaked.cc) 页面上的成员列表逐一核对；同时检查 `turtle:forward()` 这类误用 `:` 的写法、**全局变量赋值**和**未知全局变量**（拼写错误如 `pirnt`）。
- 新增和修改的示例（三协程看板、进度条、显示器界面、聊天框发中文、显示链接器、状态保存等）在 [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) 里运行过，跑的是真实的 CC: Tweaked 1.120.2 代码；部分旧示例（仓储统计、熔炉、分拣、海龟隧道、多扬声器播放器、HTTP 客户端、登录终端、认证服务器）在模拟环境中验证过重试、外设断开、重放攻击等分支。
- 模组外设的说明来自实机测试（cct-run 的联合测试 3、4），标明了模组版本；其他版本可能不同，Skill 会引导模型先在游戏里用 `peripheral.getMethods` 核对。
- 每次推送由 GitHub Actions（[`.github/workflows/validate.yml`](.github/workflows/validate.yml)）自动运行校验，并打包 `CCT_prompt_pack.zip`。
- 静态校验只能保证"能编译、全局 API 名字存在"，不能保证游戏内行为。与官方文档示例的已知出入见 `references/config-and-versions.md` 最后一节。

运行校验（需要 Python 3.8+ 与 Lua 5.2，例如 `apt install lua5.2`；首次运行需联网下载 tweaked.cc 页面并缓存到 `.cache/`）：

```bash
python3 scripts/validate_skill.py
```

## 致谢

- [cc-tweaked/CC-Tweaked](https://github.com/cc-tweaked/CC-Tweaked) 与 [tweaked.cc](https://tweaked.cc)——模组本体与官方文档
- [dan200/ComputerCraft](https://github.com/dan200/ComputerCraft)——原版 ComputerCraft
- 结构参考 [SuperFactoryManager_LLM_skill](https://github.com/EvergardenRoxy/SuperFactoryManager_LLM_skill)

## 许可证

[MIT](LICENSE) © 2026 EvergardenRoxy

本仓库仅包含说明文档与校验脚本，不包含 CC: Tweaked 模组本身的代码；CC: Tweaked 遵循其自身的许可证。

---

<a id="english"></a>

## English

An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that teaches Claude to write, review and debug Lua programs for the Minecraft mod **CC: Tweaked** (ComputerCraft): computers, turtles, pocket computers, monitors, modems, inventories, rednet/GPS, redstone and HTTP. The skill content is written in Chinese and is based on the official documentation at [tweaked.cc](https://tweaked.cc). Rather than handing the model finished programs to imitate, it teaches how to derive a program from the user's constraints (hard limits of the CC world, structure selection, failure-mode analysis, reusable design patterns, threat modelling for security, reviewing third-party tutorials). It covers the execution model (events, yielding, events lost during peripheral calls), the Lua 5.2 (Cobalt) runtime differences, the full API reference, peripherals, field-tested notes for mod peripherals (Create, Advanced Peripherals, kept apart from CC: Tweaked itself), Chinese text handling, monitor UI design, turtles, networking, a template library of 14 complete programs, an engineering guide for larger applications (reliable async HTTP, installers/updaters, settings, hot-plugging), a pre-delivery checklist, troubleshooting guides, and testing guidance for the companion tool [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) (with its MCP server, the model runs programs on a headless CC: Tweaked before delivering them, and with the cct-live mod it can test on the user's real in-game computers; without it, the model reminds the user once that it can be installed). All `lua` code blocks are syntax-checked with a Lua 5.2 compiler, their global API calls are verified against tweaked.cc, and global assignments or unknown globals are rejected; CI runs the validator on every push.

Install with Claude Code:

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

The skill follows the open [Agent Skills](https://agentskills.io) format, so it also works in other tools — copy the whole `skills/minecraft-cc-tweaked/` folder (including `references/`) into:

| Tool | User-level directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| OpenAI Codex / Cursor / VS Code Copilot / Gemini CLI | `~/.agents/skills/` (shared by all four) |
| Cherry Studio | Settings → Skills → install from folder or ZIP |

See [INSTALL.md](INSTALL.md) for per-tool details and [CONTENTS.md](CONTENTS.md) for the file list (both in Chinese). Current version: 1.2.2 ([release notes](RELEASE_NOTES.md)).

Licensed under [MIT](LICENSE). Content was produced with generative-AI assistance and reviewed by the maintainer.
