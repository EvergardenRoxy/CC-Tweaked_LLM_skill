# 入门与开发环境：新手最常卡住的地方

> 面向第一次接触 CC 的用户。回答新手问题时先确认他卡在哪一层（在哪里输入、怎么读文档、怎么编辑文件），再给代码。

## 目录

- 三个"输入的地方"
- 怎么读官方文档的函数签名
- 用外部编辑器写代码
- 在游戏外测试
- 关于中文资料与翻译
- 新手常见错误

---

## 三个"输入的地方"

| 位置 | 看起来像 | 能输入什么 | 例子 |
|---|---|---|---|
| CraftOS 命令行（shell） | `> ` 提示符 | **程序名**和参数 | `ls`、`edit mine.lua`、`mine 10`、`go forward 3`、`refuel all` |
| Lua 交互环境 | 在 shell 输入 `lua` 后的 `lua> ` | **一行行 Lua 代码**，立即执行并显示返回值 | `turtle.forward()`、`peripheral.getNames()` |
| 程序文件 | 用 `edit 文件名` 打开的编辑器 | 完整程序，保存后在 shell 里输入文件名运行 | `edit tunnel.lua` → 输入 `tunnel` 运行 |

- 在 shell 里直接输入 `turtle.forward()` 会报 `No such program`——shell 把它当成程序名了。要么先输入 `lua` 进入交互环境，要么写进文件运行。所以"turtle 命令只能写在文件里"并不准确：交互环境里也能直接调用，非常适合试验单个函数。
- 退出 `lua` 交互环境：输入 `exit()`。
- 很多常用操作已经有现成程序：`go`（移动海龟）、`turn`、`excavate`/`tunnel`、`refuel`、`equip`、`label`、`peripherals`。`help` 查看帮助，`programs` 列出全部程序。

## 怎么读官方文档的函数签名

以 `turtle.getItemDetail([slot [, detailed]])` 为例：

- **圆括号 `()` 是调用必须写的**：`turtle.forward()` 才会执行；只写 `turtle.forward` 得到的是函数本身，什么也不发生。
- **方括号 `[ ]` 表示可选参数**，不用写方括号本身：`turtle.getItemDetail()`、`turtle.getItemDetail(3)`、`turtle.getItemDetail(3, true)` 都对。
- `[limit=64]` 表示可选且默认值为 64。
- 参数后面的类型（`number`、`string`）和"Returns"部分告诉你返回几个值；海龟函数大多返回 `成功?, 原因`。
- 大小写敏感：`turtle.forward()` 对，`Turtle.Forward()` 错。

## 用外部编辑器写代码

游戏内 `edit` 能用，但长程序用外部编辑器更舒服：

1. 在游戏里对计算机执行 `id`，记下计算机 ID（海龟同理）。
2. 文件实际存放在存档里：单人游戏为 `.minecraft/saves/<存档名>/computercraft/computer/<ID>/`（整合包启动器的游戏目录可能不同）；专用服务器为 `<服务器目录>/<世界名>/computercraft/computer/<ID>/`。软盘在同级的 `disk/<软盘ID>/`。
3. 用 VS Code 等编辑器直接打开这个文件夹编辑并保存，回到游戏运行即可，**不需要重进存档**。正在运行的程序不会自动重新加载，需要重新运行。
4. VS Code 可以安装名为 **ComputerCraft** 的扩展，为 CC 的 API 提供代码补全和说明（安装后打开 `.lua` 文件即可）。
5. 多人服务器上没有存档访问权限时：用 `pastebin`/`wget` 下载程序，或使用支持远程编辑的工具。

## 在游戏外测试

- 社区有可以在电脑上直接运行 CraftOS 的模拟器（如 CraftOS-PC），适合调试界面和逻辑；海龟、模组外设等与世界交互的部分仍需进游戏验证。
- 纯逻辑部分（解析、计算、状态机）可以写成独立模块，在模拟器或普通 Lua 5.2 中先测通。

## 关于中文资料与翻译

- 官方文档 <https://tweaked.cc> 只有英文。机器翻译常出错（例如把 `up()` 译成"往前移动"），本 Skill 中的中文说明是对照原文逐条核对的。
- 官方的一句话摘要偶尔也有笔误：`turtle.getFuelLevel()` 的摘要写着 "maximum amount"，但它实际返回**当前**燃料量（最大值是 `getFuelLimit()`）。以函数的详细说明和实际行为为准。
- 网上的中文教程可能基于很老的 ComputerCraft 版本，或包含不存在的函数（如 `textutils.sha256`）。照用之前对照 `api-reference.md` 核对。

## 新手常见错误

| 现象 | 原因 | 解决 |
|---|---|---|
| shell 里输入 `turtle.forward()` 报 `No such program` | shell 只运行程序 | 先输入 `lua`，或写进文件 |
| 海龟函数返回 `false` 不动 | 没燃料 | `refuel all` 或在程序里 `turtle.refuel()`；`turtle.getFuelLevel()` 查看 |
| 程序名输入后 `No such program` | 不在当前目录或拼错 | `ls` 查看；带上路径 |
| 改了文件但运行的还是旧逻辑 | 程序在改之前就已经运行 | Ctrl+T 停止后重新运行 |
| `attempt to call nil` | 函数名拼错/大小写错/该设备没有此 API | 对照文档；普通计算机没有 `turtle` |
| `edit` 里不知道怎么保存 | 菜单需要按 Ctrl 打开 | Ctrl → 选 Save → Exit |
| 开机想自动运行 | 需要启动文件 | 把程序保存为 `startup.lua` 或在其中 `shell.run("程序")` |
