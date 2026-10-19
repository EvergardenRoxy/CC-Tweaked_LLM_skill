[English](README.md)

# CC: Tweaked LLM Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI-Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](#ai-制作声明)

> 让 Claude（及其他 LLM）正确地编写、审查和调试 Minecraft **CC: Tweaked（ComputerCraft）** Lua 程序的 Agent Skill。

[CC: Tweaked](https://tweaked.cc) 是 ComputerCraft 的现代分支，为 Minecraft 加入可编程的计算机、海龟（turtle）和各种外设。它的 Lua 环境和桌面 Lua 不同：运行在 Cobalt（Lua 5.2）上，由事件和让出（yield）驱动，按方向或网络名访问外设，海龟移动要消耗燃料。只凭旧教程或记忆写代码的模型，常会调用不存在的函数、混淆 `:` 与 `.`、丢失事件，或写出无法编译的 Lua 5.3 语法。

本仓库把执行模型、API、外设、海龟、网络、设计模式与排错方法整理成 AI 可以遵循的指南。核心 API 以官方文档 [tweaked.cc](https://tweaked.cc) 为准；用户实际安装的模组、服务器配置和整合包中实际生效的配方，决定这些指南如何落地。

**设计理念：先拆解、对齐目标，再写代码。** Skill 引导 AI 选择能解决问题的最简单方案：现有游戏机制、ROM 自带程序、短脚本，最后才是完整应用。用户已经说明的条件不再重复询问；需求明确时直接实现，只有缺失的信息会改变方案时才提问。界面、日志框架和认证系统只在任务需要时添加。

**教思路，而不是只给答案。** Skill 讲解约束、结构选择、失败模式与可组合的模式：与会让出的工作协程分开的响应式输入监听、有界队列、确认动作真正生效、配方档案，以及重启后的对账。每个示例都写明适用范围；熟悉的配方或某一次测试通过，都不会被当成所有环境通用的规则。

<a id="ai-制作声明"></a>
<a id="ai-production-disclosure"></a>

> [!IMPORTANT]
> **AI 制作声明：CC: Tweaked LLM Skill 采用生成式 AI 参与内容编写、代码校验与文档撰写。** AI 生成或修改的内容由项目维护者审阅、验证并承担最终维护责任。

> **当前发行版：[v1.3.1](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/tag/v1.3.1)**（2026-10）。文档质量修订版：重新组织 `SKILL.md`，恢复 v1.3.0 改写时丢失的 CC:T 具体指导，并用清楚的语言重写全部 26 篇参考文档、中英文 README 和安装说明。详见[中文发行说明](RELEASE_NOTES.zh-CN.md)或 [English release notes](RELEASE_NOTES.md)。

---

## 能做什么

| 场景 | 示例提问 |
|---|---|
| 编写程序 | “统计有线网络中各箱子的物品数量，显示到显示器上。” |
| 海龟自动化 | “写一个隧道挖掘程序：限定范围、检查燃料、满了回去卸货，移动中断后能恢复。” |
| 网络与远程控制 | “用 rednet 控制一路红石输出，并报告指令是否执行完成。” |
| 模组机器与工厂 | “用实际的 Create 外设和我整合包里的配方控制这条产线。” |
| 看板与触摸界面 | “做一个显示器面板，轮询箱子时也能响应触摸。” |
| 审查程序 | “检查这段 ComputerCraft 程序有没有调错 API、物品计数是否正确。” |
| 排查故障 | “解释 `attempt to index nil` 或 `Too long without yielding` 报错。” |
| 测试与实机排错（需兼容工具） | “用 cct-run 运行，并分清哪些结果来自 fixture、哪些来自游戏。” |

交付内容包括整体思路、所需设备及名称、代码、安装与运行方法，以及做过哪些验证。详略随任务规模调整，小修改不会引入应用框架。

## Skill 内容

Skill 采用**渐进式加载**：`SKILL.md`（204 行）包含工作流程、规则、执行模型、速查表、常见错误、交付格式、参考索引和交付前检查清单；AI 只在任务需要时读取 26 篇专题参考。Create 与 Advanced Peripherals 的接口说明和 CC:T 本体分开，并对应具体审查过的 jar。

参考文档涵盖 API、外设、事件、状态与恢复、配方、海龟、网络、界面与文字编码、应用工程、安全、模式、测试和排错。模组指南基于 Minecraft 1.21.1 / NeoForge 下的 Create 6.0.10 与 Advanced Peripherals 1.21.1-0.8.2a。可选集成（AE2、Refined Storage、Mekanism 等）需要安装对应模组。

详见 [Skill 内容一览](CONTENTS.md)和[完整参考索引](skills/minecraft-cc-tweaked/SKILL.md#reference-map)。历史原始资料保存在 `archive/`，不属于安装的 Skill，也不进入提示词包。

## 安装

本 Skill 遵循开放的 [Agent Skills](https://agentskills.io) 格式。把整个 `skills/minecraft-cc-tweaked/` 文件夹（**包括 `references/`**）安装到客户端的 Skill 目录。Claude Code 中：

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

支持导入压缩包的客户端可下载 [CCT_prompt_pack.zip](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.1/CCT_prompt_pack.zip)，其根目录包含 `SKILL.md` 和 `references/`；可用发行版附带的 [SHA256SUMS](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.1/SHA256SUMS) 核对校验和。

[安装与升级](INSTALL.md)说明了目录安装和压缩包导入方法，包括 Codex。各客户端的支持情况和路径不同，以客户端文档为准。升级时整体替换文件夹，避免新旧参考文件混用。

## 使用

安装后，让 AI 使用本 Skill 处理 CC:T 任务；是否自动调用取决于客户端。视情况提供：

- CC:T 版本（在 `lua` 提示符中运行 `print(_HOST)`）、Minecraft 版本、加载器和相关模组版本。
- 设备类型、外设布局或网络名，以及想要的结果。
- 现有代码和完整报错，包括文件名和行号。
- 生产线任务：整合包中当前实际的配方，以及程序允许执行哪些机器操作。

### 配套测试工具（可选）：cct-run

[cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) 是独立的测试运行时和 MCP 服务器（`cct-run mcp`）。它在 Minecraft 之外用真实的 CC:T 代码运行程序，模拟 CC:T 自带外设，并按脚本返回模组外设的结果，让 AI 在交付前检查报错、trace 和画面。

安装兼容的 cct-live 并获得你的授权后，AI 还能排查指定的游戏内电脑。这些工具都是可选的：Skill 本身不安装任何模组，也不连接游戏。各类测试能证明什么、不能证明什么，见[测试指南](skills/minecraft-cc-tweaked/references/testing.md)。

### 验证记录

| 检查项 | 结果与范围 |
|---|---|
| 静态检查 | 14 个 Lua 代码块：Lua 5.2 语法、选定的官方 API 名称与全局变量 |
| 校验器回归测试 | 10 项，覆盖正文、链接、代码围栏、Unicode 数据与离线模式 |
| 可靠性示例（v1.3.0） | cct-run / CC:T 1.120.2 中 22 项断言及看板输入处理 |
| 模组适配器（v1.3.0） | 17 项脚本化断言和 trace 检查，不执行 Java 模组 |
| 提示词包 | 27 个 Markdown 文件；检查路径、CRC 及与源文件的字节一致性 |

早期的联合测试为恢复、事件和编码相关指南提供了经验，但其中的耗时、装置布局、权限和配方数值，不代表其他环境下的性能或兼容性。范围说明见[模组核对记录](docs/mod-evidence/1.21.1/README.md)和[发行说明](RELEASE_NOTES.zh-CN.md)。

## 准确性说明

- [`scripts/validate_skill.py`](scripts/validate_skill.py) 用 Lua 5.2 编译所有 Lua 代码块，对照 [tweaked.cc](https://tweaked.cc) 检查选定的核心 API 成员，并找出全局变量和点号/冒号误用。在宿主机上编译通过不等于完全兼容 Cobalt。
- 模组指南把类文件/反编译依据、脚本化适配器测试和真实游戏观察分开记录。生成索引里出现的方法名，既不说明参数格式，也不保证在某个游戏里可用。
- 服务器当前的数据和配置可能覆盖 jar 自带的配方与默认值。搬运物料前，先查出实际可用的方法，再验证相关行为。
- [GitHub Actions](.github/workflows/validate.yml) 在每次推送和拉取请求时校验 Skill 并构建提示词包。静态检查和脚本化 fixture 不能证明游戏物理、显示效果或所有恢复路径。

使用 Python 和 Lua 5.2 编译器运行校验与打包：

```bash
python3 scripts/validate_skill.py
python3 scripts/test_validator.py
python3 scripts/package_skill.py
```

首次校验会把官方 API 页面缓存到 `.cache/`，之后可加 `--offline`。安装了兼容的 cct-run 时，可运行从参考文档中提取的示例：

```bash
python3 scripts/test_examples.py --cct-run /absolute/path/to/cct-run
python3 scripts/test_mod_examples.py --cct-run /absolute/path/to/cct-run
```

## 致谢

- [cc-tweaked/CC-Tweaked](https://github.com/cc-tweaked/CC-Tweaked) 与 [tweaked.cc](https://tweaked.cc)：模组本体与官方文档。
- [dan200/ComputerCraft](https://github.com/dan200/ComputerCraft)：原版 ComputerCraft。
- [SuperFactoryManager_LLM_skill](https://github.com/EvergardenRoxy/SuperFactoryManager_LLM_skill)：本仓库结构的参考。

## 许可证

[MIT](LICENSE) © 2026 EvergardenRoxy

本仓库包含指南文档、证据记录和校验脚本，不包含 CC:T 模组本体；CC:T 及文中提到的其他项目遵循各自的许可证。
