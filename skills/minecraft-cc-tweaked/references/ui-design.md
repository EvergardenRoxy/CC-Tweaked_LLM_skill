# 显示器界面设计

> 返回 [SKILL.md](../SKILL.md) 第 1 节。显示器的 API 见 `peripherals.md`“显示器”；中文见 `chinese-text.md`。

用户说“做个看板”“加个触摸界面”时读本文件。界面的好坏要由用户看了才算数：**先按下面的规则做出能用的版本，再请用户截图确认**，不要自己反复猜。

## 先确定尺寸和用途

- 用 `mon.getSize()` 取字符数（随 `setTextScale` 变化：缩放 1 时一格显示器约 7×5 个字符，0.5 时翻倍），按实际尺寸设计，不要假设 51×19。尺寸变化会触发 `monitor_resize`。
- 问清：谁看、在多远看（远处看用大字号）、要不要触摸（只有**高级显示器**能触摸）、哪些信息最重要。
- CC 的显示器只有 16 种颜色、每格一个字符，不能显示中文（`chinese-text.md`）。

## 布局规则（来自实测反馈）

联合测试 4 里，用户对 AI 做的显示器界面提了三轮意见：“面板太丑”→“条完全不对齐，比上个方案更丑”→“按钮太小、挤在一起”→ 改成下面的做法后“好多了”。规则如下：

1. **所有行共用一套列位置**：标签列、数值列、进度条的起点和宽度、数字列，在一个表里定义一次（下例的 `L`），每一行都用它。不要每行各自算位置。
2. **进度条等宽**：同一组进度条起点相同、宽度相同；数字（百分比、`12/16384`）放在进度条**右边的固定列**，右对齐。数字写在“条的末尾之后”会让每条长度不同，看起来不齐。
3. **左侧边栏放导航和操作**：固定宽度、和主面板颜色不同；条目从配置的列表生成（新增一条产线，边栏自动多一个按钮），条目超过高度时分页。
4. **按钮是一整行色带，文字居中，按钮之间空一行**。两行高的按钮把文字放在上面一行，看起来“字被挤到上沿”；要更大的按钮就用三行、文字放中间一行。
5. **组与组之间空一行**，同一组内不空行，全屏保持一致的节奏。
6. **文字和底色要有对比**：深色或饱和色底（蓝、灰、黑）配白字，浅色底配黑字；浅灰底上的小字容易看不清。状态色固定含义：绿 = 正常，黄 = 注意，红 = 故障，灰 = 不可用。
7. **数字输入用加减按钮**：`[-100] [-10] [ 数量 ] [+10] [+100]`，中间的数字只显示；限制上下限；另有“确认”按钮。默认值要合理（不要默认 1）。
8. **不可用的按钮显示成灰色**，并在旁边或状态栏说明原因（例如“主人不在附近”），不要点了没反应。

## 按钮：画和点用同一张表

按钮的位置只写一次：画的时候登记到 `buttons` 表，触摸时用同一张表判断点中了哪个。这样改布局时点击区域自动跟着变，不会出现“看到的按钮和能点的位置对不上”。

```lua
-- Monitor dashboard layout: one table of column positions for every row,
-- buttons that are drawn and hit-tested from the same list, fixed-width bars.
local mon = peripheral.find("monitor") or error("No monitor attached", 0)
mon.setTextScale(1)

local L = { side = 18, label = 21, value = 31, bar = 31, num = 0 }   -- column of each element
local state = { lines = { "sheet", "flour" }, selected = 1, qty = 64, stress = 0.42, progress = 0.75 }
local buttons = {}

local function put(x, y, text, fg, bg)
    mon.setCursorPos(x, y)
    if bg then mon.setBackgroundColour(bg) end
    mon.setTextColour(fg or colours.white)
    mon.write(text)
end

local function band(x, y, w, bg)                       -- a full-width coloured row
    put(x, y, (" "):rep(w), colours.white, bg)
end

local function button(x, y, w, label, bg, action)
    band(x, y, w, bg)
    put(x + math.floor((w - #label) / 2), y, label, colours.white, bg)
    buttons[#buttons + 1] = { x1 = x, x2 = x + w - 1, y = y, action = action }
end

local function bar(y, ratio, colour)
    local w, x = L.num - L.bar - 1, L.bar
    local fill = math.floor(math.max(0, math.min(1, ratio)) * w + 0.5)
    band(x, y, w, colours.grey)
    if fill > 0 then band(x, y, fill, colour) end
    put(L.num, y, ("%3d%%"):format(math.floor(ratio * 100 + 0.5)), colours.white, colours.black)
end

local function draw()
    local w, h = mon.getSize()
    L.num = w - 4                                      -- numbers in one right-hand column
    buttons = {}
    mon.setBackgroundColour(colours.black)
    mon.clear()
    band(1, 1, w, colours.blue)
    put(2, 1, "ORDER CONSOLE", colours.white, colours.blue)

    for i = 1, h - 1 do put(1, i + 1, (" "):rep(L.side), colours.white, colours.grey) end
    for i, name in ipairs(state.lines) do              -- sidebar: one row per item, blank row between
        local bg = i == state.selected and colours.lightBlue or colours.blue
        button(2, 2 + i * 2, L.side - 2, name, bg, function() state.selected = i end)
    end
    button(2, h - 1, L.side - 2, "PAUSE", colours.green, function() state.paused = not state.paused end)

    put(L.label, 3, "PROGRESS", colours.lightGrey, colours.black)
    bar(3, state.progress, colours.lime)
    put(L.label, 5, "STRESS", colours.lightGrey, colours.black)
    bar(5, state.stress, state.stress > 0.95 and colours.red or state.stress > 0.8 and colours.yellow or colours.lime)

    put(L.label, 7, "QTY", colours.lightGrey, colours.black)
    local x = L.value                                  -- [-100] [-10] [ qty ] [+10] [+100]
    local function step(n)
        button(x, 7, 5, ("%+d"):format(n), colours.blue, function()
            state.qty = math.max(1, math.min(10000, state.qty + n))
        end)
        x = x + 6
    end
    step(-100)
    step(-10)
    put(x, 7, ("%5d"):format(state.qty), colours.black, colours.white)
    x = x + 7
    step(10)
    step(100)
end

local function touched(x, y)
    for _, b in ipairs(buttons) do
        if y == b.y and x >= b.x1 and x <= b.x2 then b.action() return true end
    end
    return false
end

draw()
while true do
    local _, _, x, y = os.pullEvent("monitor_touch")
    if touched(x, y) then draw() end
end
```

- 这个例子只响应触摸，所以用单个事件循环。还要轮询外设（箱子、模组机器）时，按 `events-and-concurrency.md` 用 `parallel` 把监听触摸和读外设分开，否则触摸会丢。
- 显示器方法不等待，可以在任何协程里画。整屏重画会闪烁时，先画到隐藏的 `window`（`window.create(mon, 1, 1, w, h, false)`），画完 `setVisible(true)`；或者只重画变化的行。
- 刷新频率：状态变化时重画，加上每秒一次的定时刷新就够了。

## 进度条和绘图字符

**更细的进度条和图形**：终端和显示器只认 CC 自带的 256 个字符，Unicode 字符（包括盲文点字、方块元素）会按 UTF-8 字节显示成 2～3 个乱码。CC 自己的字符 128～159（`"\128"`～`"\159"`）是 2×3 小方块组合的绘图字符：每个字符的 6 个小格里，右下格总是背景色，其余 5 格按字符编号决定用文字色还是背景色。用它们可以把精度提高到半格（横向 2 份、纵向 3 份）；需要完整的像素绘图时可以用社区库（如 pixelbox），先核对它们的许可证。

```lua
-- Progress bar with half-cell steps: "\149" is the drawing character whose
-- left column (3 of its 6 pixels) is in the text colour, the rest background.
local function bar(target, x, y, width, ratio, fill, empty)
    ratio = math.max(0, math.min(1, ratio))
    local halves = math.floor(ratio * width * 2 + 0.5)
    local full = math.floor(halves / 2)
    target.setCursorPos(x, y)
    target.setBackgroundColour(fill)
    target.write((" "):rep(full))
    target.setBackgroundColour(empty)
    if halves % 2 == 1 and full < width then
        target.setTextColour(fill)
        target.write("\149")
        full = full + 1
    end
    target.write((" "):rep(width - full))
end

local mon = peripheral.find("monitor") or error("No monitor attached", 0)
bar(mon, 1, 1, 10, 0.75, colours.lime, colours.grey)
bar(mon, 1, 2, 10, 0.95, colours.red, colours.grey)
```

## 调色板

- **自定义调色板**（`setPaletteColour`）可以做出深色主题等效果，但会一直保留到重启。程序退出（含报错、Ctrl+T）时恢复：

```lua
local target = peripheral.find("monitor") or term.current()
local saved = {}
for i = 0, 15 do
    local c = 2 ^ i
    saved[c] = { target.getPaletteColour(c) }
end

local function restore_palette()
    for c, rgb in pairs(saved) do target.setPaletteColour(c, table.unpack(rgb)) end
end

local function main()
    target.setPaletteColour(colours.black, 0x101014)
    target.setPaletteColour(colours.grey, 0x2C2C32)
    target.setBackgroundColour(colours.black)
    target.clear()
    sleep(3)
end

local ok, err = pcall(main)
restore_palette()
if not ok and err ~= "Terminated" then printError(err) end
```

## 怎么检查界面

- **模拟器（cct-run）**：摘要里的 `monitors` 是每行的文字（没有颜色），用来检查对齐、截断和越界；`cct_screen` 可以看某一刻的画面；用时间线注入 `monitor_touch` 检查按钮。
- **实机（cct-live）**：`cct_live_screen` 加 `regions: true` 能看到色块区域和按钮位置，`colors: true` 看颜色。
- **好不好看，请用户截图**：文字记录看不出颜色、比例和字体效果。联合测试 4 里，用户发来截图后，AI 两分钟就找到了“字被挤到上沿”的原因，而此前凭文字猜了三轮。能看图的模型直接看截图；不能看图时，请用户描述哪里不对。
