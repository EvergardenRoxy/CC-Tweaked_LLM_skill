> 历史归档，暂停作为当前 Skill 指令使用。来源：main `ac32d80`；仅调整返回核心指南的链接，正文保留。

# Create（机械动力）模组的外设与机械行为

> 返回 [SKILL.md](../../../skills/minecraft-cc-tweaked/SKILL.md) 第 1 节。**本文件是 Create 模组的内容，不是 CC: Tweaked 本体。** 用户没装 Create 时不要用。

Create 自带 CC: Tweaked 集成：它的一些方块接上电脑（直接相邻或经有线调制解调器）后就是外设。方法名和行为**随 Create 版本变化**；下面是实测记录，用之前按 `peripherals.md`“模组外设的通用排查方法”在用户的游戏里核对。

**实测环境**：Minecraft 1.20.1 Forge、CC: Tweaked 1.120.2、Create 6.0.8。来源：cct-run 的联合测试 3（两次）和联合测试 4（一次，含后续调整）。其他版本可能不同。

## 外设方法

| 外设（`peripheral.getType` 的类型名） | 方法 | 实测结果 |
|---|---|---|
| 应力表 `Create_Stressometer` | `getStress()`、`getStressCapacity()` | 单位 SU。应力超过容量时整个传动网络停转，转速读数变为 0 |
| 转速表 `Create_Speedometer` | `getSpeed()` | 带符号的 rpm，负数是反转 |
| 转速控制器 `Create_RotationSpeedController` | `getTargetSpeed()`、`setTargetSpeed(rpm)` | 带符号；`setTargetSpeed` 不返回任何值（写完再 `getTargetSpeed` 核对）；超出 ±256 时**静默截断**；设成 0 即停止 |
| 显示链接器 `Create_DisplayLink` | `getSize()`、`setCursorPos(x, y)`、`getCursorPos()`、`write(文本)`、`writeBytes(字节表)`、`clearLine()`、`clear()`、`update()`、`isColor()` | 把文字写到它指向的显示目标（显示板、告示牌等），见下文 |
| 物品保险库 `create:item_vault` | 通用 `inventory` 方法 | 格子数随保险库大小变化（实测见过 1080 和 1620 格），用 `size()` 读，不要写死；`list()` 只返回非空格 |
| 创造板条箱 `create:creative_crate` | 通用 `inventory` 方法 | 物品永远不会用完：测“缺料”要请玩家换成普通箱子 |

## 显示链接器（Display Link）和显示板

显示链接器是 Create 的方块：玩家拿着它右键一个显示目标（通常是 Create 的**显示板 Display Board**，可以拼成大块的黄色信息板），再把它放好。用有线调制解调器连到电脑后，电脑就能往那个目标上写字，相当于一块远处的“告示屏”。

- **显示板能显示中文，CC 的显示器不能**：要在工厂里给人看中文信息，可以用它。
- **中文要用 `writeBytes(字节表)`**：实测 `write("中文")` 和 `writeBytes("中文")`（传字符串）都是乱码；把 UTF-8 字节放进一个表再传给 `writeBytes` 显示正常。原理见 `chinese-text.md`。
- `getSize()` 实测返回 `6, 22`，程序按“6 行、每行最多 22 个字符”写，显示正常：**第一个值是行数**，和 `term.getSize()` 的（宽, 高）顺序相反。以实际显示板为准，第一次写的时候请玩家看一眼。
- `setCursorPos` 不检查范围（写到第 60 列也不报错，只是看不见），自己把文字截到 `getSize()` 以内。
- 写完调用 `update()` 把内容推到显示目标上。内容没变就不要重写：每次刷新都重写会让显示板一直翻动。
- **显示板要有转速才会更新**（它是机械方块）：实测程序空闲时把整个传动网络设为 0 rpm 后，显示板停在旧内容上。显示板和产线共用传动时，空闲时只断开产线（离合器），保持主轴转动；或者给显示板单独供能。

```lua
-- Write UTF-8 text to a Create display board through a display link.
local link = peripheral.find("Create_DisplayLink") or error("No display link found", 0)

local function to_bytes(s)
    local t = {}
    for i = 1, #s do t[i] = s:byte(i) end
    return t
end

local last = {}
local function show(lines)
    local rows = link.getSize()                  -- first value: number of rows
    local changed = false
    for y = 1, rows do
        if (lines[y] or "") ~= (last[y] or "") then changed = true end
    end
    if not changed then return end               -- do not rewrite an unchanged board
    link.clear()
    for y = 1, rows do
        link.setCursorPos(1, y)
        link.writeBytes(to_bytes(lines[y] or ""))
        last[y] = lines[y]
    end
    link.update()
end

-- In a real program these strings can be written in Chinese in the source file
-- (saved as UTF-8); escapes are used here only to keep the example ASCII.
show({ "\232\174\162\229\141\149 3", "Stress 42%" })
```

## 机械行为（写控制程序前要知道）

这些是 Create 的游戏机制，不是 CC 的：

- **离合器（Clutch）通红石时是断开的**：用电脑或红石继电器输出红石 = 这条线**停止**，不输出 = 运行。凭直觉写会把开关弄反。
- **转速越高，应力越大**：机器的应力 = 应力系数 × 转速。实测一条粉碎轮线全速就占满 100%，两条线同时全速（24576 SU）超过容量（16384 SU）后整网停转。所以“开工”不能直接设成最高转速，过载保护要能降速，几条线能不能同时开要按应力算。
- **转速带符号**：反转是负数；目标转速和实际转速可能不同（正在加速，或者过载停转）。
- **先测清楚哪个外设真正起作用**：
  - 实测里一个转速控制器改成 0 后产量不变，另一个降一半后产量减半：名字和玩家的描述不一定对应真正控制产线的那个。
  - 原料箱的数量在生产时也可能不变（机器其实从别处取料）。这时“缺料”不能看原料数，要看产物是否还在增长。
  - 做法：逐个改变设置（转速、离合器），读应力表、转速表和产物数量的变化，用数据确认后再写进程序和配置。

## 测试时

- 在模拟器里用 cct-run 的 `scripted` 外设描述这些方块，数值取自实机（见 `testing.md`）；机器之间的联动（调高转速、应力跟着变）模拟器不会自动产生，要用时间线安排。
- 过载、缺料、拆外设这类情况要请玩家在游戏里真的做一次。
