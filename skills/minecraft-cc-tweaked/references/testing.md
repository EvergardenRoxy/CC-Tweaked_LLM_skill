# 测试程序：cct-run 模拟器与实机工具（MCP）

> 返回 [SKILL.md](../SKILL.md) 第 2.4 节

本 Skill 的配套测试工具是 [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP)：

- **模拟器**：不开 Minecraft，在真实的 CC: Tweaked 1.120.2 代码上运行程序，返回结构化的结果和完整记录。
- **实机工具**（可选）：配合 cct-live mod，接管用户正在运行的游戏里的真实电脑。

它通过 MCP 服务器（`cct-run mcp`）或命令行提供给 AI。

**先判断当前属于哪种情况（第 1 节），再按对应的一节做。**

---

## 1. 判断有没有测试环境

看你**当前可用的工具列表**（不要凭记忆猜）：

| 你能看到的 | 情况 | 按哪一节做 |
|---|---|---|
| 名字含 `cct_run`、`cct_trace`、`cct_guide` 的工具（客户端可能加前缀，如 `mcp__cct-run__cct_run`） | **有 MCP 模拟器** | 第 3 节 |
| 另外还有 `cct_live_computers`、`cct_live_attach` 等 `cct_live_*` 工具 | **还能接管实机** | 第 3 节 + 第 4 节 |
| 没有这些工具，但你能执行终端命令，而且 `cct-run version`（Windows：`cct-run.bat version`）能输出含 `"cc_tweaked"` 的 JSON | **有命令行模拟器** | 第 3 节（工具换成同名命令，见第 3.4 节） |
| 都没有 | **只有本 Skill** | 第 2 节 |

只检查一次，在第一次需要测试的时候检查。不要为了检查而去安装软件或修改用户的配置。

---

## 2. 只有 Skill、没有测试环境：提醒用户安装

这时你无法运行程序，只能靠本 Skill 的自检清单（第 6 节）和用户在游戏里手动验证。

**在第一次交付程序时**，在回答末尾提醒一次（同一段对话里不要每次都重复；用户说不需要就不再提）：

```text
【测试环境（可选）】这次的程序没有经过实际运行测试，只按自检清单检查过。
如果安装 cct-run，我可以在交付前先在真实的 CC: Tweaked 代码上运行程序，
自动检查报错、事件和外设调用，不需要打开 Minecraft：
  - 下载与安装：https://github.com/EvergardenRoxy/CC-Tweaked_MCP （见 README 的“安装”一节；只需要 Java 17+；
    如果还没有发布包，按“从源码构建”一节构建）
  - 在 AI 客户端里配置 MCP：命令 `cct-run mcp`（README 有 Claude Code、Codex 等客户端的写法）
  - 想让我直接在你的游戏里调试，还可以装 cct-live mod（同一仓库的 mod/README.md）
```

然后照常给出【怎么验证】：让用户先在 `lua` 交互环境里试单个调用，再运行程序，并说明看到什么就说明正常。

不要假装测试过，不要写“已测试通过”。

---

## 3. 有模拟器：交付前先测试

### 3.1 什么时候测

- **交付程序前**：每个要交给用户的程序都至少运行一次。
- **用户报错时**：先用模拟器重现，再改。
- **改完之后**：用同一个 fixture 再跑一次，确认修好了，也没有引入新的问题。

一行就能回答的问题（比如“怎么前进 10 格”）不需要测。

### 3.2 怎么测

1. **第一次使用前读说明**：`cct_guide`。如果客户端会截断长结果，就分节读：`section: 1` 到 `6` 是模拟器部分，`7` 是实机部分。同一段对话里读一次就够。
2. **准备 fixture**，用来模拟程序需要的外设和世界：箱子、显示器、能量/流体存储、有线网络、红石输入、预置文件，以及按 tick 注入的事件（按键、显示器触摸、红石变化、`terminate`）。格式见 `cct_guide` 第 5 节。**fixture 要符合用户描述的真实布局**（外设所在的面、网络名、物品），不要为了让测试通过而编造条件。
   - **模组外设**（Create、Advanced Peripherals 等）：如果 `cct_guide` 第 5 节有 `scripted` 外设（cct-run 新版本），用它描述：类型名，以及每个方法返回什么（`returns`、`sequence`、`error`，`sets` 让设置方法改变读取方法的返回值），时间线的 `method` 动作可以在某一刻改变返回值（比如让应力超过 95%）。数值要来自实机：`cct_live_peripheral`、`cct_live_trace` 里的 `peripheral_return`，或用户在 `lua` 里查到的结果；不要凭记忆编。它默认按会等待的方法处理，所以“外设调用期间丢事件”的问题在模拟器里也会出现。没有这个功能时，模组外设只能在实机上测；在测试程序里用 Lua 替身（覆盖 `peripheral.call`）也能跑通逻辑，但替身调用不会进 trace、不会等待，**测不出事件丢失**，测试结论里要写明。
   - **模组事件**（如聊天框的 `chat`）用时间线的 `event` 注入，参数顺序必须照搬实机记录里的真实事件。要注入 UTF-8 文字（如 `messageUtf8`），把每个字节写成不超过 U+00FF 的转义（`"\u00e5\u00b7\u00a5"` 是“工”）；直接写中文的话，程序收到的是 `?`（和游戏里 Java 传来的文字一样）。
   - **测“指令会不会丢”**：在程序读外设的那几个 tick 里注入指令事件（多发几条、错开 tick），再查有没有对应的动作（见第 5 步的 `contains`）。
3. **运行** `cct_run`：用 `file`（路径）或 `code`（源码），加上 `fixture`、`args`、`timeout`。
4. **读结果**：
   - `status`：`ok`、`error`、`timeout`、`shutdown` / `reboot`、`out_of_memory`；
   - `error.message` 和 `traceback`（带 `文件:行号`）；
   - `screen`、`monitors`（最终画面）；
   - `notes`（失败的外设调用等）。
   程序本身出错是正常的测试结果，不是工具故障。不会停止的程序以 `timeout` 结束，要通过画面和 trace 判断它是否正常。
5. **查原因要看记录，不要猜**：`cct_trace` 按 `kind` 筛选（`event`、`peripheral_call` / `peripheral_return`、`redstone_output`、`output`），或按 `ticks` 看某段时间；新版本还可以用 `contains` 按文字找（方法名、指令、屏幕上的字，如 `contains: "setTargetSpeed"`）；`cct_screen` 可以看某一刻的画面。读记录时注意：
   - 事件记录的 `args` 从事件名之后开始：`args[1]` 是 `{ os.pullEvent() }` 里的 `ev[2]`。改下标之前先在 Lua 一侧数清楚。
   - **trace 里有这条事件，不代表程序收到了**：在 `sleep`、带过滤的 `os.pullEvent`、会等待的外设方法期间到达的事件会被丢掉，trace 照样记录。对照事件的 tick 和程序当时在等哪次外设调用（`peripheral_call` 到 `peripheral_return` 之间）。
   - `peripheral_call` 的 `main_thread: true` 表示这个方法会等待。
6. **修改后重新运行**，直到结果符合预期。每轮只改一处，避免搞不清是哪处改动起了作用。

### 3.3 怎么写进回答

在【怎么验证】里写清楚测了什么、结果如何，以及**模拟没有覆盖到的部分**：

```text
【测试】已在 cct-run（CC: Tweaked 1.120.2 模拟）中运行：
  - 正常情况：显示器显示 3 种物品合计，status ok；
  - 箱子断开：报出 "No chest found"，status error（符合预期）。
  模拟未覆盖：真实的模组箱子格子规则、服务器卡顿；请在游戏里再确认一次。
```

模拟器**不支持**以下内容，涉及时要明确告诉用户“这部分没有测到”：
- 海龟、口袋电脑、命令电脑；
- 真实世界（方块、区块加载、卡顿）；
- HTTP 和 WebSocket；
- 扬声器、打印机、磁盘驱动器、无线 / 末影调制解调器；
- 游戏内时间（固定为 0）；
- 容器的格子规则；
- 模组外设只有 fixture 里写的返回值（`scripted`），机器之间不会联动（调高转速不会让应力跟着变，除非时间线这样安排）。

完整清单见 `cct_guide` 第 6 节。

### 3.4 命令行方式

没有 MCP、只有命令行时，各工具对应同名命令：

| MCP 工具 | 命令 |
|---|---|
| `cct_run` | `cct-run run 程序.lua --fixture f.json --timeout 15 -- 参数` |
| `cct_trace` | `cct-run trace latest --kind event,peripheral_call` |
| `cct_screen` | `cct-run screen latest --tick 40` |
| `cct_guide` | `cct-run guide` |

命令的输出是 JSON，退出码的含义：0 正常结束，1 Lua 错误，2 超时，3 关机或重启，4 内存耗尽，64 和 65 表示参数或输入有误。

---

## 4. 有实机工具：在用户的游戏里测试和排错

`cct_live_*` 工具会操作用户**真实的**游戏。模拟器测不到的内容（海龟、HTTP、无线、真实外设和真实世界）在这里测，用户在游戏里遇到的问题也在这里查。第一次使用前读 `cct_guide`，参数 `section: 7`。

### 4.1 规则

- **只在用户要求或同意时才接管**，并且只接管用户指定的那台电脑。接管时用户会在聊天栏看到提示，可以随时用 `/cctlive detach <id>` 收回。如果工具返回 `revoked`，立即停止，并先问用户再说。
- **输入、点击、开关机、写文件和 `cct_live_lua` 都会改变用户的世界**：只做用户同意的操作。`cct_live_lua` 的代码拥有这台电脑的全部权限，没有得到同意时只做只读检查。不要为了“测试”而删除或覆盖用户的文件。
- `terminate` 等同于玩家长按 Ctrl+T：程序会结束，或者跳出事件循环、去执行后面的代码，这可能暴露出平时走不到的问题。没有必要时不要发；发了的话，要在报告里说明之后的现象是它引起的。
- **测完恢复原状**：改动文件之前先 `cct_live_snapshot {op: "save"}` 保存快照；结束时用 `diff` 看改动了什么，用 `restore` 恢复，再 `diff` 一次确认 `identical`，并在报告里写明。不要自己去复制存档文件夹。没有快照工具时（旧版本），自己写入的临时文件要删除，改动过的文件要还原。
- 写文件需要用户在 mod 的配置里打开 `files.allow_write`（`cct_live_attach` 返回的 `files_write` 会告诉你是否已打开）。没打开就请用户手动修改，不要劝用户打开。
- **实机验证要真实发生**：用 `cct_live_event` 注入的聊天、触摸事件，参数是你自己排的，只能证明程序能处理你构造的事件，**不能算实机验证**。聊天指令请用户在聊天栏里真的输入；过载、缺料、拆外设这类情况，告诉用户具体怎么做（加机器、换箱子、拆下应力表），等用户做完再看结果。做不到的（例如原料是创造模式的无限箱子）就在报告里写“只在模拟器里测过”，不要用注入事件冒充。报告里分清：实机真实发生 / 实机注入 / 只在模拟器 / 没测。
- **用完就释放**：`cct_live_detach`。

### 4.2 省 token：每次工具返回的内容都会一直留在上下文里

- 检查状态用 `cct_live_status`（返回很小）；等待用 `cct_live_wait`（在服务端等待，只占一次调用）。**不要自己 sleep 之后反复看屏幕。**
- 查 trace 时先用 `summary: true` 看各类记录的数量，再用 `kind` + `after: <seq>` 只取需要的那一段。
- `cct_live_screen` 默认只返回文字；只有需要找按钮时才加 `regions: true`，需要颜色时才加 `colors: true`。
- **在电脑上查事实用 `cct_live_lua`**：一次调用就能运行一段 Lua，拿到打印内容和返回值，比如文件大小、用 `load()` 检查语法、`peripheral.getMethods`。临时文件会自动删除。不要再手动“写脚本 → 运行 → 读输出 → 删除”，那样一个事实要花 4 次调用，还容易在被测电脑上留下文件。超时时会返回 `pending` 名字，之后用 `cct_live_lua {result: 名字}` 取回结果，不要重新运行。
- 想知道服务器到底返回了什么：`handle` 记录里如果有 `body: N`，用 `cct_live_body` 读完整正文，不用自己再去请求一遍。
- 只关心某个文件或 URL 时，给 `cct_live_trace` 传 `contains`（例如 `contains: "User.lua"`），一次拿到它的请求、读取和写入记录；只关心某个外设或方法时，新版本可以传 `peripheral` / `method`（有线网络上的外设按网络名记录，`via` 是调制解调器所在的面）。
- **程序运行时读外设**：如果有 `cct_live_peripheral`，用它直接读取（例如应力表的 `getStress`），不经过电脑的 Lua，不影响正在运行的程序，也不用先停掉程序；它只允许读取类方法。没有它时 `cct_live_lua` 只能在 shell 提示符下用。
- 想看 CC 自带的程序和 API 源码（如 `rom/apis/peripheral.lua`），新版本的 `cct_live_files` 可以只读地读 `/rom`；否则去 CC: Tweaked 仓库的 tag `v1.20.1-1.120.2` 读（`cct_guide` 开头有链接格式），不要猜分支名。

### 4.3 流程

1. `cct_live_computers` 找到电脑，然后 `cct_live_attach`（长时间测试时可以传 `lease_seconds`），记下返回的 `last_seq` 和 `monitors`。如果之后要改动文件，先 `cct_live_snapshot {op: "save"}`。
2. 执行操作：
   - `cct_live_type`：输入 shell 命令或程序需要的文字，可以一次输入多行。
   - `cct_live_click`：点击图形界面的按钮。先用 `regions` 找到区域：按钮单独成块时，点区域的 `center`；按钮和外面的卡片颜色相同时，整张卡片会被合成一个区域，这时要点区域里 `labels`（按钮标签）的 `center`。点显示器时加 `source`。
   - 如果电脑旁边有显示器，程序的主界面可能显示在显示器上：`cct_live_attach` 会返回 `monitors`，查看时给 `cct_live_screen` / `cct_live_status` 传 `source`。
3. `cct_live_wait`：等屏幕出现某段文字、出现某类记录（`printed_error`、`http_failure`、`vm_close`），或者画面停止变化。等文字时注意：旧版本会直接匹配操作之前就在屏幕上的文字（例如重启后等 `>`，匹配到的是重启前的提示符，程序其实还没启动）；新版本只认操作之后变化过的屏幕。拿不准时改等 `kind`（如 `vm_start`），或者等一段只有新状态才会出现的文字。
4. `cct_live_status {after}` 看发生了什么，再用 `cct_live_trace {kind, after}` 只读需要的记录。每条记录都有 `seq`（在 trace 里的顺序）和 `tick`（游戏时间）：`after` 按 seq 筛选，`ticks` 按 tick 筛选。读记录时注意：
   - **程序崩溃先看 `printed_error`**（shell 就是这样报告错误的；用了 `bg` / `fg` 多标签时，`program` 可能是标签页的启动程序，以错误文字里的文件名为准）；`vm_error` 只记录 Too long without yielding 这类 VM 级错误；
   - 网络和文件看 `api`（请求了什么 URL、打开了什么文件）和 `handle`（读写的数据，以及 `bytes`，即数据的完整长度）；
   - 外设看 `peripheral_call` / `peripheral_return`；事件看 `event`，`args` 从事件名之后开始（`args[1]` 是 `ev[2]`），字符串是程序实际收到的样子（新版本），中文显示成 `?` 就说明程序收到的也是 `?`；
   - trace 有大小上限：结果里出现 `first_seq` 或 `trace_rotated`（新版本）表示更早的记录已被丢弃，旧版本出现 `truncated` 后就不再记录。长时间测试时以程序自己的日志和屏幕为准。
5. 需要看完整文件时用 `cct_live_files op=read`，需要在电脑上做检查时用 `cct_live_lua`，需要看 HTTP 响应的完整内容时用 `cct_live_body`。
6. 结论要以记录为依据，写明对应的记录类型和 tick（例如“tick 2081 的 handle readAll 读到 `<!doctype html>`”）。改动过文件的话，先用快照恢复（见 4.1），然后 `cct_live_detach`（它会顺便清理 `/.cctlive` 里的临时文件）。

### 4.4 模拟器和实机怎么分工

| 需要验证的内容 | 用什么 |
|---|---|
| 语法错误、运行时错误、Too long without yielding、事件丢失、外设调用逻辑、显示器界面、红石 | 先用模拟器（快，可以反复跑，不影响用户的世界） |
| 海龟、HTTP/WebSocket、无线 rednet、真实模组外设、区块加载、真实时间 | 实机（用户同意时） |
| 模组外设的程序逻辑（保护阈值、指令、看板、事件丢失） | 先在实机上查清方法和真实数值，写成 `scripted` fixture，在模拟器里反复测；最后在实机上请用户配合确认 |
| 用户在游戏里看到的报错 | 用实机看真实的记录；修复后先在模拟器里验证（能模拟的部分），再在实机上确认 |
