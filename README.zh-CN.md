[English](README.md)

# CC: Tweaked LLM Skill

帮助 AI 智能体设计、编写、审查和调试 Minecraft **CC: Tweaked（ComputerCraft）** Lua 程序的编程 Skill，涵盖电脑、海龟、外设与模组自动化。

**当前发行版：[v1.3.0](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/tag/v1.3.0)。** 活动 Skill 及参考文档统一使用英文，本页提供中文使用说明。

## 内容范围

- CC:T 核心 API、外设发现、物品栏、流体、能量、红石与海龟编程。
- 响应式事件处理、有界队列、状态持久化、中断恢复与实际完成验证。
- 终端和显示器界面、文字编码、rednet、GPS、HTTP 与 WebSocket。
- Create 动力、应力、显示、物流、包装与列车。
- Advanced Peripherals 聊天、传感器、玩家背包、存储桥接、可选扩展及 Create 集成。
- 依据**当前整合包实际生效的配方**设计生产控制，不预设原料、循环次数或成功率。

模组指南基于已审查的 Minecraft 1.21.1 / NeoForge 下 Create 6.0.10 与 Advanced Peripherals 1.21.1-0.8.2a 附件。使用示例前需核对现场接口、配置与有效配方；可选集成需要安装对应模组。

## 安装

从发行版下载 [CCT_prompt_pack.zip](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/CCT_prompt_pack.zip)，导入支持 Skill 压缩包的客户端。ZIP 根目录包含 `SKILL.md` 与 `references/`。

使用目录安装时，将完整的 [`skills/minecraft-cc-tweaked`](skills/minecraft-cc-tweaked/SKILL.md) 文件夹（包含 `references/`）放入客户端支持的 Skill 目录。例如 Codex 项目级目录可使用 `.agents/skills/minecraft-cc-tweaked/`。

Claude Code 用户可将本仓库添加为插件市场，再通过插件界面安装 `minecraft-cc-tweaked@cct-llm-skills`。

详见[安装与升级](INSTALL.md)。升级时整体替换 Skill，保持核心文档与参考文件一致。

## 使用

向智能体说明使用本 Skill 处理 CC:T 任务，并按需提供游戏及模组版本、设备布局、现有程序或报错，以及预期结果。例如：

- “审查这个库存控制器是否存在丢事件或搬运计数错误。”
- “依据这个整合包的实际配方与外设，编写 Create 产线控制程序。”
- “排查 Advanced Peripherals 聊天指令为何在重启后失效。”

本 Skill 提供编程指导，不安装 Minecraft 模组，也不附带游戏连接或测试运行时。智能体可以使用已有的兼容工具，并应区分模拟检查与真实游戏观察。

## 文档导航

| 文档 | 内容 |
|---|---|
| [Skill 入口](skills/minecraft-cc-tweaked/SKILL.md) | 工作方法与完整参考索引 |
| [内容总览](CONTENTS.md) | 主题范围 |
| [安装说明](INSTALL.md) | 安装布局与升级 |
| [发行说明](RELEASE_NOTES.md) | v1.3.0 变更与验证 |
| [模组核对记录](docs/mod-evidence/1.21.1/README.md) | 附件基线与可重现的方法索引 |

`archive/` 保留历史原文以便追溯，不参与活动 Skill 加载或提示词包打包。

## 开发与校验

```bash
python3 scripts/validate_skill.py
python3 scripts/test_validator.py
python3 scripts/package_skill.py
```

校验需要 Lua 5.2 编译器以及从 tweaked.cc 缓存的官方 API 页面。缓存齐全后可使用 `--offline`。已安装兼容的 [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) 时，还可运行：

```bash
python3 scripts/test_examples.py --cct-run /absolute/path/to/cct-run
python3 scripts/test_mod_examples.py --cct-run /absolute/path/to/cct-run
```

文档示例测试检查 CC:T 运行时与脚本化模组边界，不执行所附 Java 模组，也不证明 Minecraft 中的加工或显示效果。CI 会校验 Skill 并构建提示词包。

## 许可

参见 [LICENSE](LICENSE)。
