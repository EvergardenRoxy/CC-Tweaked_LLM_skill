# 发行版说明：来自两次实机联合测试的修正

这一版根据 cct-run 的联合测试 3（Create 工厂控制中心，两次，两个不同的 AI 模型）修正和补充了 Skill。两次测试里，AI 花时间最多的都是同一个问题：**外设方法在等待服务器执行时，期间到达的聊天指令、触摸和计时器事件会被丢掉**。而 Skill 原来推荐的“单一事件等待点”结构，恰好会让这个问题出现。测试记录见 cct-run 仓库的 `docs/joint-test-factory-report.md`。

## 修改

- **事件丢失（最重要）**：
  - `SKILL.md` 第 7 条铁律、执行模型、结构选择表、常见错误表和自检清单：会等待的外设方法（箱子/储罐/能量方块的通用方法、大多数模组外设方法）和 `sleep` 一样会丢事件；既要轮询外设又要响应指令时，用 `parallel` 把只收事件的监听协程和调用外设的协程分开。
  - `events-and-concurrency.md` 新增“外设调用会丢事件：看板 + 指令的标准结构”：现象、在 cct-run 里的实测（单循环 20 条指令只处理 11 条、计时器丢失后看板冻结；三协程结构 20 条全部处理）、经过测试的三协程模板。另外写明了 `ev[1]` 是事件名、`os.clock()` 和 `os.epoch("utc")` 的区别。
  - `design-thinking.md`：修正了模式 1“单一事件等待点”（处理分支里调用会等待的外设方法时，它不能保证不丢事件）、结构选择表和硬约束表。
  - `templates.md`：修正模板 1“要响应触摸时改为事件循环”的建议。
- **模组外设**（`peripherals.md`）：
  - 共同点：U+00FF 以上的字符（中文）从模组传进 Lua 时变成 `?`；同一外设直接贴着又经有线网络接入时，事件到达两次；怎么判断一个方法会不会等待。
  - Create 6.0.8 和 Advanced Peripherals 0.7.48r（Minecraft 1.20.1）的实测记录：应力表、转速表、转速控制器（静默截断到 ±256、无返回值）、聊天框（`chat` 事件的参数顺序、`messageUtf8`、`sendMessageToPlayer` 的 `utf8Support`、`getOperationCooldown` 必须带参数）、玩家探测器（参数顺序）、物品保险库、创造板条箱。
- **测试**（`testing.md`）：
  - 模组外设用 cct-run 新版本的 `scripted` fixture 描述（数值来自实机）；没有时用 Lua 替身的局限（测不出事件丢失）。
  - 读 trace 的注意事项：`args` 从事件名之后开始；trace 里有的事件不代表程序收到了；`main_thread`；`contains`。
  - **实机验证要真实发生**：注入的聊天、触摸事件不算实机验证，要请玩家真的操作；报告里分清真实发生、注入、只在模拟器、没测。
  - cct-run 新版本的工具：`cct_live_peripheral`（程序运行时读外设）、只读 `/rom`、trace 的 `peripheral` / `method`、`cct_live_wait` 不再匹配旧画面、trace 轮换。
- **社区建议**：
  - `peripherals.md` 和 `SKILL.md` 4.7：用 CC 自带的绘图字符 128～159 做半格精度的进度条（附经过测试的示例），不要用 Unicode 方块或盲文字符。
  - `app-engineering.md`：一个函数最多 200 个 `local`（在模拟器里验证过报错信息）；解决办法是模块表和拆文件，不是全局变量（`bios.strict_globals` 会让全局变量赋值报错）。
- **`troubleshooting.md`**：新增 4 条（看板冻结/指令丢失、模组文字变 `?`、聊天指令执行两次、200 个 `local` 的上限），修改第 49 条。

## 校验

`scripts/validate_skill.py` 全部通过：60 个 Lua 代码块。新增的三协程模板和进度条示例另外在 cct-run（CC: Tweaked 1.120.2）里运行过：三协程模板在轮询箱子的同时处理了全部 30 条注入的触摸和聊天指令。

## 已知限制

- Create / Advanced Peripherals 的实测记录只来自一个版本组合；其他版本要按 `peripherals.md` 的步骤重新核对。
- `scripted` fixture、`cct_live_peripheral` 等需要 cct-run 的新版本；Skill 里都写了“没有时怎么办”。

## 升级方法

用新的 `skills/minecraft-cc-tweaked/` 文件夹替换旧的；需要上传 zip 的客户端，按 INSTALL.md 重新打包再上传。

---

## 上一版：加入测试引导（配合 cct-run）

这一版让 Skill 学会**在交付程序前先测试**。AI 会先判断当前有没有测试环境，再按对应的方式处理：

- **只有 Skill**：照常交付程序，并在第一次交付时提醒用户，可以安装测试环境 [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP)。
- **有 cct-run 模拟器**：交付前先在真实的 CC: Tweaked 1.120.2 代码上运行程序，根据记录排错，并在回答里如实写出测了什么、哪些部分没有测到。
- **还装了 cct-live mod**：在用户同意后，接管用户游戏里的真实电脑，测试模拟器测不到的内容（海龟、HTTP、无线网络、真实的模组外设），也用来排查用户在游戏里遇到的问题。

没有安装 cct-run 时，Skill 的其他内容和以前完全一样，不需要做任何改动。

### 新增

- **`references/testing.md`**，新的参考文件：
  1. **判断有没有测试环境**：根据当前可用的工具列表判断，不凭记忆猜；在第一次需要测试时检查一次。
  2. **只有 Skill 时的安装提醒**：给出现成的提醒文字，同一段对话里只提醒一次；用户说不需要，就不再提。
  3. **模拟器测试流程**：
     - 什么时候测：交付前、用户报错时、改完之后；
     - fixture 要符合用户描述的真实布局；
     - 先看记录再下结论；
     - 每轮只改一处；
     - 回答里的【测试】一节怎么写，模拟器不支持哪些内容。
  4. **实机测试规则**：
     - 只在用户同意时接管，收到 `revoked` 立即停止；
     - 尽量不发 `terminate`；
     - 改动文件前先用 `cct_live_snapshot` 保存快照，测完恢复原状并确认，再释放电脑；
     - 省 token 的用法（`status` / `wait` / `summary` / trace 的 `contains` / `cct_live_lua` 和超时后的 `result` / `cct_live_body`）；
     - 怎么读记录（程序崩溃先看 `printed_error`）；
     - 模拟器和实机怎么分工。
  - 也写了只有命令行、没有 MCP 时的对应命令。

### 修改

- **`SKILL.md`**（现在大约 450 行）：
  - 新增第 19 条铁律“能测先测”：有测试环境时，交付前必须运行；没有时，不能声称“已测试”。铁律现在一共 20 条。
  - 参考文件索引里加了 `testing.md`。
  - 新增第 2.4 节，说明各种测试环境分别怎么用。
  - 回答模板里加了【测试】一行。
  - 自检清单和设计推导的第 6 步都加了测试相关的内容。
- **`references/getting-started.md`**：提到可以用 cct-run 测试程序。
- **`README.md`**：
  - “能做什么”里加了测试和实机排错的例子；
  - 新增“配套测试环境（可选）：cct-run”一节；
  - 更新了文件结构和英文摘要。
- **`INSTALL.md`**：
  - zip 的文件结构里加上了 `testing.md`；
  - 新增“配合 cct-run 使用”一节：Claude Code、使用 `mcpServers` JSON 的客户端和 Codex 的 MCP 配置写法，cct-live mod 的安装，以及怎么确认已经配置好。

### 升级方法

用新的 `skills/minecraft-cc-tweaked/` 文件夹替换旧的。需要上传 zip 的客户端，按 INSTALL.md 重新打包 `CCT_prompt_pack.zip` 再上传。**一定要包含 `references/testing.md`**，否则 AI 找不到测试说明。

想让 AI 真正运行程序，还需要另外安装 cct-run（需要 Java 17+），见 INSTALL.md 的“配合 cct-run 使用”一节。

### 兼容性

- 内容以 CC: Tweaked 1.120.2（Minecraft 1.20.1）为准。程序本身的写法仍然适用于其他较新的版本，但 cct-run 只模拟 1.120.2。
- 测试引导只用到 MCP 工具名，不依赖特定的 AI 客户端。客户端给工具名加了前缀（例如 `mcp__cct-run__cct_run`）也能识别。

### 校验

`scripts/validate_skill.py` 全部通过：58 个 Lua 代码块的 Lua 5.2 语法检查和 API 核对通过，13 个参考文件的链接都有效。

### 已知限制

- 测试引导要等和 cct-run 联合实测之后才能确认效果；测试方案见 cct-run 仓库的 `docs/joint-test.md`。
- 模拟器测不到的内容（海龟、HTTP、真实世界等），AI 会在回答里注明“这部分没有测到”。没有 cct-live 时，这部分仍需要用户在游戏里自己验证。

### 许可证

MIT。
