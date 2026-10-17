# Skill 内容一览

Skill 采用**渐进式加载**：触发时只加载精简的核心文件（约 330 行），细节文件由模型在需要时按索引读取，避免每次占用大量上下文。

**核心文件** [`SKILL.md`](skills/minecraft-cc-tweaked/SKILL.md)（每次触发时加载）

| 章节 | 内容 |
|---|---|
| 0. 铁律 | 给 AI 的 18 条硬约束（先拆解与对齐、Lua 5.2、不编造 API 并分清 CC 本体与模组、`.` 与 `:`、外设命名、检查返回值、必须让出、外设调用丢事件、稀疏表、燃料、区块加载与不覆盖 `startup.lua`、中文、工程化、不照搬模板、安全代码需用户同意、能测先测……） |
| 1. 参考文件索引 | "遇到什么情况读哪个文件"的路由表 |
| 2. 协助流程 | 先拆解与对齐目标、需要问清的信息、六步设计推导、两段式回答模板（先确认方案，再交付程序与可选增强） |
| 3. 执行模型 | CraftOS 启动流程、事件队列、yield、外设调用耗时、程序结构选择 |
| 4. API 速查 | Lua 5.2 差异、外设基础、常用写法速查表（细节在参考文件）、状态保存示例、版本敏感特性 |
| 5. 最常见的错误 | 14 条高频错误与正确写法 |
| 6. 自检清单 | 交付前逐条核对（含长期运行/大型程序的附加项） |

**参考文件** [`references/`](skills/minecraft-cc-tweaked/references)（按需读取）

| 文件 | 内容 |
|---|---|
| `design-thinking.md` | **设计方法**：先拆解与找最简单方案、六步推导流程、CC 硬约束清单、结构选择、失败模式五问、12 个思路模式、评审代码/教程的方法、完整推导示例 |
| `security.md` | 何时使用（仅在用户要求/同意时加入安全代码）、威胁模型（网络旁观者/能操作终端/能拆机/OP）、各机制能挡住什么、常见教程误区、加盐迭代哈希（附经测试向量验证的纯 Lua SHA-256）、本地登录终端、挑战-应答远程认证 |
| `getting-started.md` | 新手入门：shell/`lua` 交互环境/程序文件的区别、读懂文档签名、外部编辑器与文件位置、模拟器、中文资料的可信度 |
| `testing.md` | **测试**：判断有没有测试环境；只有 Skill 时提醒用户安装 cct-run；有 cct-run 模拟器时交付前用 fixture 运行、读结果和 trace、如实写出模拟没覆盖的部分；有实机工具（cct-live）时规范接管、省 token 的查询方式、用完释放；模组外设写成 `scripted` fixture；实机验证要请玩家真实操作，注入的事件不算；连发测试验证不丢事件；程序运行时读外设、改文件；界面请用户截图 |
| `api-reference.md` | 全局 API 完整参考：`os`、`fs`、`io`、`term`、`window`、`colors`、`textutils`、`settings`、`shell`、`redstone`、`parallel`、`vector`、`commands`、`cc.*` 库 |
| `peripherals.md` | CC 本体的外设：连接与命名、通用外设（inventory/fluid/energy）、物品与方块详情字段、显示器、扬声器、打印机、驱动器、红石继电器；模组外设的通用排查方法和共同点 |
| `mod-create.md` | **Create 模组**（非 CC 本体）的实测记录：应力表、转速表、转速控制器、显示链接器与显示板（`writeBytes` 显示中文、要有转速才更新）、物品保险库；离合器、应力与转速的关系，怎么确认哪个外设真正起作用 |
| `mod-advanced-peripherals.md` | **Advanced Peripherals 模组**（非 CC 本体）的实测记录：聊天框（事件参数、`messageUtf8`、用 JSON 文本发中文、冷却）、玩家探测器 |
| `chinese-text.md` | 中文能去哪里（终端/显示器不能；聊天框、显示板能）、Lua 字符串是字节、Java 与 Lua 之间的转换、测试里注入中文、utf8display 点阵字体库 |
| `ui-design.md` | 显示器界面：尺寸、共用列位置、等宽进度条、侧边栏、按钮画与点用同一张表、数字加减输入、绘图字符、调色板、请用户截图确认 |
| `turtle.md` | 海龟全部函数、燃料、工具升级、可靠移动封装、坐标跟踪、物品栏管理、常见任务要点、区块加载 |
| `networking.md` | rednet、modem、GPS 星座搭建、HTTP/WebSocket、安全提示 |
| `events-and-concurrency.md` | 全部事件参数表、事件循环、计时器、`parallel`、**外设调用会丢事件（看板 + 指令的三协程结构，附实测）**、协程、`terminate`、性能 |
| `templates.md` | 14 个参考程序及其背后的设计决策表（仓储统计、熔炉阵列、分拣、伐木、隧道、农场、遥控、触摸面板、能量控制、储罐、密码门、网络音乐、断点续跑、多扬声器同步播放器） |
| `app-engineering.md` | 大型程序工程化：模块结构、可靠的异步 HTTP（请求标记、超时看门狗、选择性重试、分块读取、Range 大文件下载）、安装器与更新器、设置持久化与校验、外设选择与热插拔、功能探测、日志脱敏、发布与 CI |
| `troubleshooting.md` | 59 条常见错误对照、报错信息速查、排错流程、游戏内工具 |
| `config-and-versions.md` | 服务器配置、`/computercraft` 命令、数据包、版本差异、Lua 兼容性、资料来源与已知出入 |

### 按主题找文件

| 想了解 | 看哪里 |
|---|---|
| CC: Tweaked 本体的 API 和外设 | `SKILL.md` 第 4 节、`api-reference.md`、`peripherals.md` |
| 模组外设（**不是 CC 本体**，各自标明了实测的模组版本） | `mod-create.md`（Create）、`mod-advanced-peripherals.md`（Advanced Peripherals） |
| 中文：显示、聊天框收发、Create 显示板 | `chinese-text.md` |
| 看板、触摸界面 | `ui-design.md`、`events-and-concurrency.md`（看板 + 指令的三协程结构） |
| 交付前测试、实机排错 | `testing.md`（需要 [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP)） |

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
│           ├── mod-create.md
│           ├── mod-advanced-peripherals.md
│           ├── chinese-text.md
│           ├── ui-design.md
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
├── CONTENTS.md                   # Skill 内容一览（本文件）
├── INSTALL.md                    # 各工具安装详解
├── RELEASE_NOTES.md              # 发行版说明
├── LICENSE
└── README.md
```

[← 返回 README](README.md) · [安装](INSTALL.md) · [发行版说明](RELEASE_NOTES.md)
