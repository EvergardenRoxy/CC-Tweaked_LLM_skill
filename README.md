# CC: Tweaked LLM Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI-Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](#ai-制作声明)

> 让 Claude（及其他 LLM）正确地编写、审查和调试 Minecraft **CC: Tweaked（ComputerCraft）** Lua 程序的 Agent Skill。

[CC: Tweaked](https://tweaked.cc) 是 ComputerCraft 的现代分支，为 Minecraft 加入可编程计算机、海龟（turtle）和各种外设，用 Lua 编程。它的运行环境与普通 Lua 差别不小：Lua 5.2（Cobalt）运行时、事件驱动、外设按方向或网络名访问、海龟要燃料……网上还有大量 1.7.10 时代的过时教程。LLM 凭记忆写出的 CC 程序经常调用不存在的函数、用错 `:` 和 `.`、在循环里忘记让出导致 `Too long without yielding`，或者用 Lua 5.3 的 `//` 直接语法错误。

本仓库提供一份**以官方文档 [tweaked.cc](https://tweaked.cc) 为准**的 Skill，把 CC: Tweaked 的执行模型、API、外设、海龟、网络、常见陷阱、程序模板和排错流程整理成 AI 可直接遵循的指南。

**设计理念：先拆解、先对齐，教思路而不是给答案。** 收到请求后，模型先拆解问题、从"不写代码 → ROM 自带程序 → 几十行脚本 → 完整系统"的阶梯里找最简单够用的方案，和用户确认目标后再写；用户没要求的功能（界面、日志、配置系统、认证）只作为"可选增强"列出。安全被视为重要话题，但认证/加密类代码**只在用户同意后**加入（Minecraft 服务器大多是可信环境），默认只在风险提示里简要说明风险和可选方案。

**教思路，而不是给答案。** 只塞给模型一堆成品程序，它只会生成相似的程序；换了设备、规模或网络条件就写错。因此本 Skill 的核心是**从需求推导程序的方法**：CC 世界的硬约束清单、程序结构的选择依据、对每个外部交互的失败模式分析、一组可组合的思路模式（单一事件等待点、按真实时间节拍、有界缓冲、执行后验证、数据驱动规则、状态对账、启动自检……），以及评审网上教程/旧代码的方法。模板只作为"某组约束下的参考答案"，并标注了"条件变了要换什么设计"。

[English summary](#english)

<a id="ai-制作声明"></a>

> [!IMPORTANT]
> **AI 制作声明：CC: Tweaked LLM Skill 采用生成式 AI 参与内容编写、代码校验与文档撰写。** AI 生成或修改的内容由项目维护者审阅、验证并承担最终维护责任。

---

## 能做什么

| 场景 | 示例提问 |
|---|---|
| 编写程序 | "用 CC 写一个仓库统计程序，把所有箱子的物品数量显示在显示器上" |
| 海龟自动化 | "写一个挖 3×3 隧道的海龟程序，背包满了自动回来卸货" |
| 网络与远程控制 | "用 rednet 做一个无线遥控器，远程开关基地的红石" |
| 审查程序 | "帮我看看这段 ComputerCraft 代码有没有问题" |
| 排查故障 | "报错 attempt to index a nil value / Too long without yielding 怎么办" |
| 外设与模组机器 | "读取能量存储方块的电量，低于 20% 自动开发电机" |
| 测试与实机排错（需要 cct-run） | "写好之后先在模拟器里跑一遍再给我" / "接管 3 号电脑，看看这个安装脚本为什么装完打不开" |

每次回答都会给出：**整体思路 + 安装清单（设备 → 位置/网络名）+ 程序 + 运行步骤 + 风险提示**，并在交付前对照内置自检清单。

## Skill 内容一览

Skill 采用**渐进式加载**：触发时只加载精简的核心文件（约 450 行），细节文件由模型在需要时按索引读取，避免每次占用大量上下文。

**核心文件** [`SKILL.md`](skills/minecraft-cc-tweaked/SKILL.md)（每次触发时加载）

| 章节 | 内容 |
|---|---|
| 0. 铁律 | 给 AI 的 20 条硬约束（先拆解与对齐、Lua 5.2、不编造 API、`.` 与 `:`、外设命名、检查返回值、必须让出、`sleep` 丢事件、稀疏表、燃料、区块加载、中文显示、工程化、不照搬模板与教程、安全代码需用户同意、能测先测……） |
| 1. 参考文件索引 | "遇到什么情况读哪个文件"的路由表 |
| 2. 协助流程 | 先拆解与对齐目标、需要问清的信息、六步设计推导、两段式回答模板（先确认方案，再交付程序与可选增强） |
| 3. 执行模型 | CraftOS 启动流程、事件队列、yield、外设调用耗时、程序结构选择 |
| 4. API 速查 | Lua 5.2 差异、外设、物品栏/流体/能量、海龟、红石、网络、终端/显示器、文件/设置、版本敏感特性 |
| 5. 最常见的错误 | 12 条高频错误与正确写法 |
| 6. 自检清单 | 交付前逐条核对（含长期运行/大型程序的附加项） |

**参考文件** [`references/`](skills/minecraft-cc-tweaked/references)（按需读取）

| 文件 | 内容 |
|---|---|
| `design-thinking.md` | **设计方法**：先拆解与找最简单方案、六步推导流程、CC 硬约束清单、结构选择、失败模式五问、12 个思路模式、评审代码/教程的方法、完整推导示例 |
| `security.md` | 何时使用（仅在用户要求/同意时加入安全代码）、威胁模型（网络旁观者/能操作终端/能拆机/OP）、各机制能挡住什么、常见教程误区、加盐迭代哈希（附经测试向量验证的纯 Lua SHA-256）、本地登录终端、挑战-应答远程认证 |
| `getting-started.md` | 新手入门：shell/`lua` 交互环境/程序文件的区别、读懂文档签名、外部编辑器与文件位置、模拟器、中文资料的可信度 |
| `testing.md` | **测试**：判断有没有测试环境；只有 Skill 时提醒用户安装 cct-run；有 cct-run 模拟器时交付前用 fixture 运行、读结果和 trace、如实写出模拟没覆盖的部分；有实机工具（cct-live）时规范接管、省 token 的查询方式、用完释放；模组外设写成 `scripted` fixture；实机验证要请玩家真实操作，注入的事件不算 |
| `api-reference.md` | 全局 API 完整参考：`os`、`fs`、`io`、`term`、`window`、`colors`、`textutils`、`settings`、`shell`、`redstone`、`parallel`、`vector`、`commands`、`cc.*` 库 |
| `peripherals.md` | 外设连接与命名、通用外设（inventory/fluid/energy）、物品与方块详情字段、显示器、扬声器、打印机、驱动器、红石继电器、模组外设排查、模组外设的共同点（中文变 `?`、接两次事件重复）与 Create / Advanced Peripherals 实测记录、CC 绘图字符做细进度条 |
| `turtle.md` | 海龟全部函数、燃料、工具升级、可靠移动封装、坐标跟踪、物品栏管理、常见任务要点、区块加载 |
| `networking.md` | rednet、modem、GPS 星座搭建、HTTP/WebSocket、安全提示 |
| `events-and-concurrency.md` | 全部事件参数表、事件循环、计时器、`parallel`、**外设调用会丢事件（看板 + 指令的三协程结构，附实测）**、协程、`terminate`、性能 |
| `templates.md` | 14 个参考程序及其背后的设计决策表（仓储统计、熔炉阵列、分拣、伐木、隧道、农场、遥控、触摸面板、能量控制、储罐、密码门、网络音乐、断点续跑、多扬声器同步播放器） |
| `app-engineering.md` | 大型程序工程化：模块结构、可靠的异步 HTTP（请求标记、超时看门狗、选择性重试、分块读取、Range 大文件下载）、安装器与更新器、设置持久化与校验、外设选择与热插拔、功能探测、日志脱敏、调色板恢复、中文显示限制与 utf8display 点阵字体库、发布与 CI |
| `troubleshooting.md` | 55 条常见错误对照、报错信息速查、排错流程、游戏内工具 |
| `config-and-versions.md` | 服务器配置、`/computercraft` 命令、数据包、版本差异、Lua 兼容性、资料来源与已知出入 |

## 安装

本 Skill 遵循开放的 [Agent Skills](https://agentskills.io) 格式：一个包含 `SKILL.md` 的文件夹（本仓库为 `skills/minecraft-cc-tweaked/`，**连同 `references/` 一起复制**）。支持该格式的工具只需把文件夹放进对应目录即可自动加载。

### 速查表

| 工具 | 项目级目录 | 用户级目录（所有项目可用） | 一键安装 |
|---|---|---|---|
| [Claude Code](INSTALL.md#claude-code) | `.claude/skills/` | `~/.claude/skills/` | `/plugin` 插件市场 |
| [Claude.ai / 桌面端](INSTALL.md#claudeai--claude-桌面端) | — | 设置中上传 zip | — |
| [OpenAI Codex](INSTALL.md#openai-codexcli--ide-插件--codex-app) | `.agents/skills/` | `~/.agents/skills/` | `$skill-installer` |
| [Cursor](INSTALL.md#cursor) | `.cursor/skills/` 或 `.agents/skills/` | `~/.cursor/skills/` 或 `~/.agents/skills/` | — |
| [VS Code + GitHub Copilot](INSTALL.md#vs-code--github-copilot) | `.github/skills/` 或 `.agents/skills/` | `~/.copilot/skills/` 或 `~/.agents/skills/` | — |
| [Gemini CLI](INSTALL.md#gemini-cli) | `.gemini/skills/` 或 `.agents/skills/` | `~/.gemini/skills/` 或 `~/.agents/skills/` | `gemini skills install` |
| [Cherry Studio](INSTALL.md#cherry-studio) | — | 设置 → 技能 | 从文件夹 / ZIP / GitHub 安装 |
| [ChatGPT、DeepSeek 等网页对话](INSTALL.md#chatgptdeepseek-等不支持-skills-的对话工具) | — | 上传文件或项目知识库 | — |

> 💡 **`.agents/skills/` 是通用目录**：Codex、Cursor、VS Code Copilot、Gemini CLI 都会读取它。同时使用多个工具时，放在 `~/.agents/skills/` 一处即可。

各工具的详细安装步骤（含 zip 打包方法）见 **[INSTALL.md](INSTALL.md)**。

## 使用

安装后无需额外操作。当你提到 CC: Tweaked、ComputerCraft、CC:T、海龟/turtle、rednet、`peripheral.wrap`、`startup.lua`、显示器等内容时，Skill 会自动触发。

建议在提问时附上：

- **CC: Tweaked 版本**（游戏里 `print(_HOST)`）与 Minecraft 版本、加载器
- 设备类型（普通/高级计算机、海龟、口袋计算机）、外设摆放位置或网络名（`peripherals` 程序可列出）
- 现有代码与完整报错（文件名:行号: 消息）

### 配套测试环境（可选）：cct-run

装上 [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) 并在 AI 客户端里配置它的 MCP 服务器（`cct-run mcp`）后，Skill 会让模型**在交付前先运行程序**：

- 在真实的 CC: Tweaked 代码上运行，不需要打开 Minecraft；
- 用 fixture 模拟箱子、显示器、红石等外设；
- 根据报错行号和事件记录修改，并在回答里如实写出测了什么、模拟没覆盖什么。

再装上 cct-live mod，模型还可以在你同意后接管游戏里的电脑，进行实机测试和排错：接管时聊天栏会提示，你可以随时用 `/cctlive detach <id>` 收回控制。

没有安装时，Skill 照常工作，只会在第一次交付程序时提醒一次可以安装。详见 [`references/testing.md`](skills/minecraft-cc-tweaked/references/testing.md)；Skill 和 cct-run 一起安装、配置的步骤见 [INSTALL.md](INSTALL.md#配合-cct-run-使用)。

## 准确性说明

- Skill 中全部 `lua` 代码块均已用 [`scripts/validate_skill.py`](scripts/validate_skill.py) 通过 **Lua 5.2 编译器**（与 CC: Tweaked 的 Cobalt 运行时同版本）的语法检查，并把其中用到的全局 API（`turtle.*`、`fs.*`、`peripheral.*`……）与 [tweaked.cc](https://tweaked.cc) 页面上的成员列表逐一核对；同时检查 `turtle:forward()` 这类误用 `:` 的写法；并从编译后的字节码中找出**全局变量赋值**（示例代码一律使用 `local`）和**未知全局变量读取**（拼写错误如 `pirnt`、`textutil`）。
- 部分代码（仓储统计、熔炉、分拣、海龟隧道、多扬声器播放器、HTTP 客户端、登录终端、认证服务器）还在模拟的 CC 环境中运行过，验证了重试、跳转、外设断开、锁定、重放攻击等逻辑分支；SHA-256 实现与标准测试向量及随机二进制输入的结果一致。
- 每次推送由 GitHub Actions（[`.github/workflows/validate.yml`](.github/workflows/validate.yml)）自动运行校验，并打包 `CCT_prompt_pack.zip` 作为构建产物。
- 静态校验只能保证"能编译、全局 API 名字存在"，不能保证外设方法和游戏内行为。涉及模组外设、槽位、服务器配置时，Skill 会引导用户在游戏内用 `peripheral.getMethods` 等方式实测。
- 与官方文档示例的已知出入、配置默认值的说明见 `references/config-and-versions.md` 最后一节。

运行校验（需要 Python 3.8+ 与 Lua 5.2，例如 `apt install lua5.2`；首次运行需联网下载 tweaked.cc 页面并缓存到 `.cache/`）：

```bash
python3 scripts/validate_skill.py
```

## 目录结构

```text
.
├── .claude-plugin/
│   └── marketplace.json          # Claude Code 插件市场清单
├── .github/workflows/
│   └── validate.yml              # CI：校验 + 打包 zip
├── skills/
│   └── minecraft-cc-tweaked/
│       ├── SKILL.md              # 核心：规则、执行模型、API 速查、自检清单
│       └── references/           # 按需读取的细节文件
│           ├── api-reference.md
│           ├── peripherals.md
│           ├── turtle.md
│           ├── networking.md
│           ├── events-and-concurrency.md
│           ├── templates.md
│           ├── troubleshooting.md
│           ├── config-and-versions.md
│           ├── app-engineering.md
│           ├── design-thinking.md
│           ├── security.md
│           ├── getting-started.md
│           └── testing.md
├── scripts/
│   └── validate_skill.py         # Lua 语法、API 名称、全局变量与结构校验
├── INSTALL.md                    # 各工具安装详解
├── LICENSE
└── README.md
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

An [Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) that teaches Claude to write, review and debug Lua programs for the Minecraft mod **CC: Tweaked** (ComputerCraft): computers, turtles, pocket computers, monitors, modems, inventories, rednet/GPS, redstone and HTTP. The skill content is written in Chinese and is based on the official documentation at [tweaked.cc](https://tweaked.cc). Rather than handing the model finished programs to imitate, it teaches how to derive a program from the user's constraints (hard limits of the CC world, structure selection, failure-mode analysis, reusable design patterns, threat modelling for security, reviewing third-party tutorials). It covers the execution model (events, yielding), the Lua 5.2 (Cobalt) runtime differences, the full API reference, peripherals, turtles, networking, a template library of 14 complete programs, an engineering guide for larger applications (reliable async HTTP, installers/updaters, settings, hot-plugging), a pre-delivery checklist, troubleshooting guides, and testing guidance for the companion tool [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) (with its MCP server, the model runs programs on a headless CC: Tweaked before delivering them, and with the cct-live mod it can test on the user's real in-game computers; without it, the model reminds the user once that it can be installed). All `lua` code blocks are syntax-checked with a Lua 5.2 compiler, their global API calls are verified against tweaked.cc, and global assignments or unknown globals are rejected; CI runs the validator on every push.

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

See [INSTALL.md](INSTALL.md) for per-tool details (in Chinese).

Licensed under [MIT](LICENSE). Content was produced with generative-AI assistance and reviewed by the maintainer.
