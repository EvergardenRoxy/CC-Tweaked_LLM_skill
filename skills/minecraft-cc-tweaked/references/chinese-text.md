# 中文：显示、收发与编码

> 返回 [SKILL.md](../SKILL.md) 第 0 节第 13 条。

## 先看结论：中文能去哪里

| 文字要去的地方 | 能不能显示中文 | 怎么做 | 属于 |
|---|---|---|---|
| CC 的终端、显示器（`print`、`mon.write`） | **不能** | 默认用英文/拼音并告诉用户原因；用户明确要中文界面时，可以用社区点阵字体库 utf8display（见下文，有前提） | CC: Tweaked 本体 |
| `error`、`printError`、程序崩溃信息、`read()` 输入 | **不能** | 只能英文 | 本体 |
| 文件内容 | 能（按 UTF-8 字节保存） | 直接写；`#s` 是字节数 | 本体 |
| Advanced Peripherals 聊天框发给玩家的消息 | 能 | `sendFormattedMessageToPlayer` + JSON 里的 `\uXXXX` 转义（`mod-advanced-peripherals.md`）；`sendMessageToPlayer` 发中文是乱码 | 模组 |
| Advanced Peripherals 聊天框收到的玩家消息 | 能 | 读 `chat` 事件的 `messageUtf8`（第 5 个参数）；普通的消息参数里中文是 `?` | 模组 |
| Create 显示链接器 → 显示板 | 能 | `writeBytes(字节表)`（`mod-create.md`）；`write("中文")` 是乱码 | 模组 |

其他模组的外设：先在游戏里试一次，请玩家确认显示是否正常，再写进程序。

## 原理：Lua 字符串是字节

- CC 的 Lua 字符串是**字节序列**。源文件里写的 `"订单"` 按 UTF-8 保存，是 6 个字节：`#"订单"` 是 6，字符数用 `utf8.len`。
- CC 的终端和显示器把每个字节当成自己字符集里的一个字符（256 个），所以 UTF-8 的中文显示成 2～3 个怪字符。
- **从模组（Java）传进 Lua 的文字**：U+00FF 以上的字符（中文等）一律变成 `?`。需要原文时找模组另外提供的 UTF-8 字段（如聊天框的 `messageUtf8`）。
- **从 Lua 传给模组的文字**：每个字节变成一个字符，UTF-8 的中文在游戏里就是乱码（例如 `å·²`）。要让模组显示中文，只能走它提供的其他通道：聊天框的 JSON 文本（`\uXXXX` 转义由游戏解析）、显示链接器的字节表（由模组按 UTF-8 解码）。
- 判断方法：在 cct-run 的 trace 里，程序传给外设的参数如果显示成 `å·²` 这样每个字节一个字符，游戏里就会是乱码。

## 在测试里用中文（cct-run）

- fixture 里注入中文事件（如聊天框的 `messageUtf8`）：把每个 UTF-8 字节写成不超过 U+00FF 的转义，例如 `"å·¥"` 是“工”。直接写中文的话程序收到的是 `?`（和游戏里 Java 传来的文字一样）；新版 cct-run 会在摘要的 `notes` 里用 `fixture_text` 提醒。
- 不要因为注入中文不方便就给程序加一套英文指令来“测试”：那样真正的中文路径没有测到。
- 程序发出的中文对不对，模拟器只能看参数的字节；最终要请玩家在游戏里看一眼。

## 中文界面：utf8display 点阵字体库（CC 显示器上显示中文的唯一办法）

用户明确想在 CC 的显示器或终端上显示中文时，可以提示使用社区库 **utf8display**（<https://git.liulikeji.cn/xingluo/ComputerCraft-Utf8/src/branch/main/utf8display>）：用 2×3 像素的图形字符拼出汉字，再用 `term.blit` 绘制。先向用户说明下面的前提，用户确认后再写：

- 需要 CC: Tweaked 1.94.0+（用到 `colors.toBlit`）；服务器开启 HTTP，且没有拦截 `git.liulikeji.cn`。
- 字体文件很大：默认的 8px 简体字体约 1.7 MB，超过计算机默认 1 MB 的硬盘，只能在每次开机后第一次显示时联网下载（之后缓存在内存里直到重启）。服主调大 `computer_space_limit` 后，才能把字体存到本地并用 `utf8display.setConfig("fontPath", 路径)` 加载。12px 字体约 4 MB。
- 占地方：8px 字体每个汉字 4 格宽 × 3 行高，51×19 的计算机屏幕一行约 12 个汉字、最多 6 行。用显示器时配合 `setTextScale(0.5)`。
- 库只画到当前的 `term`：输出到显示器要先 `term.redirect(mon)`，画完再恢复。
- 只有交给 `utf8display.print`/`write`/`blit` 的文字能显示中文。`error`、`printError`、崩溃信息、`read()` 仍然走原生终端，必须用英文；中文也无法通过 `read()` 输入。
- 字体加载失败时库会直接 `error()`，而且报错信息是中文（显示为乱码）。调用时用 `pcall` 包住，失败就退回英文显示。
- 安装：`wget https://git.liulikeji.cn/xingluo/ComputerCraft-Utf8/raw/branch/main/utf8display/utf8display.lua utf8display.lua`，程序里 `require("utf8display")`。不要用该库 README 里每次运行 `load(http.get(...).readAll())()` 的写法：明文 HTTP 下载并执行远程代码，内容随时可能变（见 `security.md`）。
- 该仓库没有许可证文件：回答里只给链接和用法，不要把库的源码复制进来。

工厂里只是想让人看到中文状态时，Create 的显示板（`mod-create.md`）往往比 utf8display 简单：不需要下载字体，也不占电脑的硬盘。

```lua
-- 中文界面示例：用户已确认使用 utf8display（前提见上）
local mon = peripheral.find("monitor") or error("No monitor attached", 0)
local has_lib, utf8display = pcall(require, "utf8display")

-- zh 用 utf8display 绘制；没装库、HTTP 关闭或字体下载失败时，用原生 print 显示 en
local function show(zh, en, fg, bg)
    if has_lib and pcall(utf8display.print, zh, fg, bg) then return end
    print(en)
end

mon.setTextScale(0.5)
local old = term.redirect(mon)
term.setBackgroundColour(colours.black)
term.clear()
term.setCursorPos(1, 1)
show("仓库状态", "Storage status", colours.yellow, colours.black)
show("铁锭: 1024", "Iron ingot: 1024", colours.white, colours.black)
term.redirect(old)
```
