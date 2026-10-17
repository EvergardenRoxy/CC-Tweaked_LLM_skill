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
3. **运行** `cct_run`：用 `file`（路径）或 `code`（源码），加上 `fixture`、`args`、`timeout`。
4. **读结果**：
   - `status`：`ok`、`error`、`timeout`、`shutdown` / `reboot`、`out_of_memory`；
   - `error.message` 和 `traceback`（带 `文件:行号`）；
   - `screen`、`monitors`（最终画面）；
   - `notes`（失败的外设调用等）。
   程序本身出错是正常的测试结果，不是工具故障。不会停止的程序以 `timeout` 结束，要通过画面和 trace 判断它是否正常。
5. **查原因要看记录，不要猜**：`cct_trace` 按 `kind` 筛选（`event`、`peripheral_call` / `peripheral_return`、`redstone_output`、`output`），或按 `ticks` 看某段时间；`cct_screen` 可以看某一刻的画面。
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
- 容器的格子规则。

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
- **测完恢复原状**：自己写入的临时文件要删除；为了实验改动过的文件要还原，并在报告里写明。
- 写文件需要用户在 mod 的配置里打开 `files.allow_write`（`cct_live_attach` 返回的 `files_write` 会告诉你是否已打开）。没打开就请用户手动修改，不要劝用户打开。
- **用完就释放**：`cct_live_detach`。

### 4.2 省 token：每次工具返回的内容都会一直留在上下文里

- 检查状态用 `cct_live_status`（返回很小）；等待用 `cct_live_wait`（在服务端等待，只占一次调用）。**不要自己 sleep 之后反复看屏幕。**
- 查 trace 时先用 `summary: true` 看各类记录的数量，再用 `kind` + `after: <seq>` 只取需要的那一段。
- `cct_live_screen` 默认只返回文字；只有需要找按钮时才加 `regions: true`，需要颜色时才加 `colors: true`。
- **在电脑上查事实用 `cct_live_lua`**：一次调用就能运行一段 Lua，拿到打印内容和返回值，比如文件大小、用 `load()` 检查语法、`peripheral.getMethods`。临时文件会自动删除。不要再手动“写脚本 → 运行 → 读输出 → 删除”，那样一个事实要花 4 次调用，还容易在被测电脑上留下文件。
- 想知道服务器到底返回了什么：`handle` 记录里如果有 `body: N`，用 `cct_live_body` 读完整正文，不用自己再去请求一遍。

### 4.3 流程

1. `cct_live_computers` 找到电脑，然后 `cct_live_attach`（长时间测试时可以传 `lease_seconds`），记下返回的 `last_seq` 和 `monitors`。
2. 执行操作：
   - `cct_live_type`：输入 shell 命令或程序需要的文字，可以一次输入多行。
   - `cct_live_click`：点击图形界面的按钮。先用 `regions` 找到区域：按钮单独成块时，点区域的 `center`；按钮和外面的卡片颜色相同时，整张卡片会被合成一个区域，这时要点区域里 `labels`（按钮标签）的 `center`。点显示器时加 `source`。
   - 如果电脑旁边有显示器，程序的主界面可能显示在显示器上：`cct_live_attach` 会返回 `monitors`，查看时给 `cct_live_screen` / `cct_live_status` 传 `source`。
3. `cct_live_wait`：等屏幕出现某段文字、出现某类记录（`printed_error`、`http_failure`、`vm_close`），或者画面停止变化。
4. `cct_live_status {after}` 看发生了什么，再用 `cct_live_trace {kind, after}` 只读需要的记录。每条记录都有 `seq`（在 trace 里的顺序）和 `tick`（游戏时间）：`after` 按 seq 筛选，`ticks` 按 tick 筛选。读记录时注意：
   - **程序崩溃先看 `printed_error`**（shell 就是这样报告错误的）；`vm_error` 只记录 Too long without yielding 这类 VM 级错误；
   - 网络和文件看 `api`（请求了什么 URL、打开了什么文件）和 `handle`（读写的数据，以及 `bytes`，即数据的完整长度）；
   - 外设看 `peripheral_call` / `peripheral_return`。
5. 需要看完整文件时用 `cct_live_files op=read`，需要在电脑上做检查时用 `cct_live_lua`，需要看 HTTP 响应的完整内容时用 `cct_live_body`。
6. 结论要以记录为依据，写明对应的记录类型和 tick（例如“tick 2081 的 handle readAll 读到 `<!doctype html>`”），然后 `cct_live_detach`。

### 4.4 模拟器和实机怎么分工

| 需要验证的内容 | 用什么 |
|---|---|
| 语法错误、运行时错误、Too long without yielding、事件丢失、外设调用逻辑、显示器界面、红石 | 先用模拟器（快，可以反复跑，不影响用户的世界） |
| 海龟、HTTP/WebSocket、无线 rednet、真实模组外设、区块加载、真实时间 | 实机（用户同意时） |
| 用户在游戏里看到的报错 | 用实机看真实的记录；修复后先在模拟器里验证（能模拟的部分），再在实机上确认 |
