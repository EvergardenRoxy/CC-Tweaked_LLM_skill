[English](README.md)

# CC: Tweaked LLM Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI-Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](#ai-制作声明)

> 让 Claude（及其他 LLM）正确地编写、审查和调试 Minecraft **CC: Tweaked（ComputerCraft）** Lua 程序的 Agent Skill。

[CC: Tweaked](https://tweaked.cc) 是 ComputerCraft 的现代分支，为 Minecraft 加入可编程计算机、海龟（turtle）和各种外设。它的 Lua 环境与桌面解释器差别不小：Cobalt、事件与让出、按方向或网络名访问外设、海龟燃料等。旧教程和模型记忆容易导致调用不存在的函数、混淆 `:` 与 `.`、丢事件，或生成不受支持的 Lua 语法。

本仓库将执行模型、API、外设、海龟、网络、设计模式与排错方法整理成 AI 可遵循的指南。核心 API 契约以官方文档 [tweaked.cc](https://tweaked.cc) 为依据；实际能力、模组实现、服务器配置和有效配方决定这些指导如何应用到当前环境。

**设计理念：先拆解、对齐目标，教会推导思路。** 从现有游戏机制、ROM 程序、短脚本到完整应用，选择最简单且足够的方案。复用用户已经提供的条件，继续已获授权的工作；仅在缺失信息影响正确性或范围时提问。界面、日志框架或认证系统按任务需要添加。

**教思路，而不是给答案。** Skill 介绍约束、结构选择、失败模式与可组合模式：响应式监听和会让出的工作协程、有界队列、执行后验证、配方配置与启动对账。示例注明适用边界；熟悉的配方或某次成功测试不能直接成为所有环境的控制规则。

<a id="ai-制作声明"></a>
<a id="ai-production-disclosure"></a>

> [!IMPORTANT]
> **AI 制作声明：CC: Tweaked LLM Skill 采用生成式 AI 参与内容编写、代码校验与文档撰写。** AI 生成或修改的内容由项目维护者审阅、验证并承担最终维护责任。

> **当前版本：[v1.3.0](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/tag/v1.3.0)**（2026-10）。活动 Skill 已改为英文，由精简核心与 26 篇参考文档组成。本版吸收可靠性测试经验，按附件基线整理 Create/AP 指南，并依据当前整合包实际生效的配方推导生产控制。详见[中文发行说明](RELEASE_NOTES.zh-CN.md)或 [English release notes](RELEASE_NOTES.md)。

---

## 能做什么

| 场景 | 示例提问 |
|---|---|
| 编写程序 | “统计有线网络中各箱子的物品数量，并显示到显示器上。” |
| 海龟自动化 | “设计有边界、燃料检查、卸货和移动中断恢复的隧道挖掘程序。” |
| 网络与远程控制 | “用 rednet 控制红石输出，并报告指令是否完成。” |
| 模组机器与工厂控制 | “根据现场 Create 外设和实际配方控制这条产线。” |
| 看板与触摸界面 | “制作轮询库存时仍能响应指令的显示器面板。” |
| 审查程序 | “检查这段 ComputerCraft 程序的 API 和搬运计数是否正确。” |
| 排查故障 | “排查 nil value 或 `Too long without yielding` 报错。” |
| 测试与实机排错，需兼容工具 | “用 cct-run 运行，并区分 fixture 结果和真实游戏观察。” |

交付应说明整体思路、所需设备与名称、程序改动、运行步骤及相关验证。细节随任务规模调整，小修改不必引入大型应用框架。

## Skill 内容

Skill 采用**渐进式加载**：97 行 `SKILL.md` 包含工作方法、证据边界、运行规则与参考索引，智能体按需读取 26 篇主题文档。Create 与 Advanced Peripherals 契约和 CC:T 本体分开，限定到已审查附件。

内容涵盖 API、外设、事件、恢复、配方、海龟、网络、界面与文字、工程、安全、模式与测试。模组指南基于 Minecraft 1.21.1 / NeoForge 下 Create 6.0.10 与 Advanced Peripherals 1.21.1-0.8.2a。可选集成需要安装对应模组。

详见 [Skill 内容一览](CONTENTS.md)和[完整参考索引](skills/minecraft-cc-tweaked/SKILL.md#reference-map)。历史原文保存在 `archive/`，不进入活动 Skill 和提示词包。

## 安装

本 Skill 遵循开放的 [Agent Skills](https://agentskills.io) 格式。将完整的 `skills/minecraft-cc-tweaked/` 文件夹（**包含 `references/`**）安装到客户端支持的 Skill 目录。Claude Code 可使用：

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

支持压缩包导入的客户端可下载 [CCT_prompt_pack.zip](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/CCT_prompt_pack.zip)，根目录包含 `SKILL.md` 与 `references/`；可用发行附件 [SHA256SUMS](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/SHA256SUMS) 核对校验和。

详见[安装与升级](INSTALL.md)，其中包含 Codex 等客户端的目录或导入说明。不同客户端支持范围与路径不同，以已安装客户端文档为准。升级时整体替换 Skill，避免混用新旧参考文件。

## 使用

安装后，可要求智能体使用本 Skill 处理 CC:T 任务。是否自动发现取决于客户端。按需提供：

- CC:T 版本（在 Lua 解释器中运行 `print(_HOST)`）、Minecraft 版本、加载器和相关模组版本。
- 设备类型、外设布局或网络名，以及预期结果。
- 现有程序与完整报错，包括文件名和行号。
- 生产任务的当前有效配方依据，以及允许的机器操作。

### 配套测试环境（可选）：cct-run

[cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) 提供独立测试运行时和 MCP 服务器（`cct-run mcp`），可在 Minecraft 外运行 CC:T 程序、模拟本体外设，并脚本化模组边界返回值。智能体可以在交付前检查错误、trace 和画面。

安装兼容的 cct-live 且获得授权后，还可排查指定的游戏内电脑。测试工具是可选项，Skill 本身不安装模组或游戏连接。证据分层与实机操作边界见[测试指南](skills/minecraft-cc-tweaked/references/testing.md)。

### 实测与验证记录

| 当前验证 | 结果与边界 |
|---|---|
| 静态检查 | 12 个 Lua 代码块；Lua 5.2 语法、选定官方 API 名称与全局变量 |
| 校验器回归 | 10 项，覆盖正文、链接、围栏、Unicode 数据与离线行为 |
| 可靠性示例 | cct-run / CC:T 1.120.2 中的 22 项断言及看板输入处理 |
| 模组适配器 | 17 项脚本化断言和 trace 检查，不执行 Java 模组 |
| 提示词包 | 27 个活动 Markdown 文件；路径、CRC 与源文件字节一致性检查 |

历史联合测试为恢复、事件和编码指南提供了经验，但其耗时、装置、授权和配方值不构成通用性能或兼容性保证。范围说明见[模组核对记录](docs/mod-evidence/1.21.1/README.md)和[发行说明](RELEASE_NOTES.zh-CN.md)。

## 准确性说明

- [`scripts/validate_skill.py`](scripts/validate_skill.py) 使用 Lua 5.2 编译活动示例，按 [tweaked.cc](https://tweaked.cc) 检查选定核心 API 成员，并检查全局变量及点号/冒号误用。宿主编译不等于完整的 Cobalt 兼容性测试。
- 模组指南区分类文件/反编译依据、脚本化适配器测试与真实游戏观察。生成索引中的方法名不代表参数契约或现场可用性。
- 当前服务器数据和配置可能覆盖 jar 默认配方与参数。控制物料前先发现实际接口，再验证相关行为。
- [GitHub Actions](.github/workflows/validate.yml) 在推送和拉取请求时校验 Skill 并构建提示词包。静态检查和 fixture 不证明游戏物理、显示效果或所有恢复窗口。

使用 Python 与 Lua 5.2 编译器运行校验和打包：

```bash
python3 scripts/validate_skill.py
python3 scripts/test_validator.py
python3 scripts/package_skill.py
```

首次校验将官方 API 页面缓存到 `.cache/`，后续可使用 `--offline`。已安装兼容 cct-run 时，可运行从文档提取的示例：

```bash
python3 scripts/test_examples.py --cct-run /absolute/path/to/cct-run
python3 scripts/test_mod_examples.py --cct-run /absolute/path/to/cct-run
```

## 致谢

- [cc-tweaked/CC-Tweaked](https://github.com/cc-tweaked/CC-Tweaked) 与 [tweaked.cc](https://tweaked.cc)——模组本体与官方文档。
- [dan200/ComputerCraft](https://github.com/dan200/ComputerCraft)——原版 ComputerCraft。
- [SuperFactoryManager_LLM_skill](https://github.com/EvergardenRoxy/SuperFactoryManager_LLM_skill)——仓库结构参考。

## 许可证

[MIT](LICENSE) © 2026 EvergardenRoxy

本仓库包含指导文档、证据记录和校验脚本，不包含 CC:T 模组本体；CC:T 和其他引用项目遵循各自许可证。
