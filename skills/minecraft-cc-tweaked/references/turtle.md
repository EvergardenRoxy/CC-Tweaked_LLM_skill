# 海龟（turtle）编程

> 来源：tweaked.cc `turtle` 模块、Item/Block details、Data packs 页面。

## 目录

- 基本事实
- 完整函数表
- 燃料
- 工具与升级
- 可靠的移动与挖掘封装
- 坐标与朝向跟踪
- 物品栏管理
- 常见任务要点（挖矿、砍树、种田、建造、合成）
- 区块加载与断点续跑

---

## 基本事实

- 海龟是一个方块，每次只能移动一格；左右移动要先转向。
- 物品栏 16 格（槽位 1–16），多数物品操作作用于**当前选中槽**（`turtle.select`）。
- 失败的动作**不报错**，返回 `false, "原因"`。官方建议检查返回值或包 `assert`：`assert(turtle.forward())`。
- 移动（前后上下）消耗 1 燃料；转向、挖掘、放置、攻击不耗燃料。
- `detect()` 中"实心"指任何非空气、非液体方块。
- 海龟可以含水，可以穿过水源/流动水移动而不破坏水源。
- 只有海龟有 `turtle` API；`if turtle then … end` 可判断当前设备是否是海龟。
- 海龟物品栏变化触发 `turtle_inventory` 事件。

## 完整函数表

| 函数 | 返回 | 说明 |
|---|---|---|
| `forward()` `back()` `up()` `down()` | `ok, 原因` | 移动；没燃料、被挡住返回 false |
| `turnLeft()` `turnRight()` | `ok, 原因` | 原地转 90° |
| `dig([side])` `digUp([side])` `digDown([side])` | `ok, 原因` | 需要能挖该方块的工具；`side` 为 `"left"`/`"right"` 指定用哪边工具 |
| `place([文本])` `placeUp` `placeDown` | `ok, 原因` | 放置当前槽方块/使用物品（桶取放液体、骨粉、播种…）；放告示牌时可写文字；**不能**按按钮、拉拉杆 |
| `attack([side])` `attackUp` `attackDown` | `ok, 原因` | 攻击实体（剑最好） |
| `detect()` `detectUp()` `detectDown()` | `bool` | 是否有实心方块 |
| `inspect()` `inspectUp()` `inspectDown()` | `has_block, 数据表或原因` | 方块 `name`、`state`、`tags` |
| `compare()` `compareUp()` `compareDown()` | `bool` | 前方方块是否与当前槽物品相同 |
| `drop([n])` `dropUp` `dropDown` | `ok, 原因` | 放进前方容器；没有容器就丢到地上 |
| `suck([n])` `suckUp` `suckDown` | `ok, 原因` | 从容器或地面掉落物吸取，默认最多一组；从当前槽开始找空位 |
| `select(槽)` | `true` | 槽位越界报错 |
| `getSelectedSlot()` | 槽号 | |
| `getItemCount([槽])` `getItemSpace([槽])` | 数字 | 默认当前槽 |
| `getItemDetail([槽 [, detailed]])` | 表或 `nil` | `detailed=true` 时信息更多但更慢 |
| `compareTo(槽)` | `bool` | 当前槽与指定槽物品是否相同 |
| `transferTo(槽 [, n])` | `bool` | 当前槽 → 指定槽 |
| `getFuelLevel()` `getFuelLimit()` | 数字或 `"unlimited"` | |
| `refuel([n])` | `ok, 原因` | 消耗当前槽燃料；`refuel(0)` 只检查能否作燃料 |
| `equipLeft()` `equipRight()` | `ok, 原因` | 当前槽物品装到左/右；旧升级放回物品栏；当前槽为空则只卸下 |
| `getEquippedLeft()` `getEquippedRight()` | 物品详情或 `nil` | 1.116.0+ |
| `craft([n=64])` | `ok, 原因` | 需要工作台升级；物品栏按 3×3 摆放（槽 1-3、5-7、9-11），**其他槽必须全空**；`craft(0)` 只检查配方 |

`turtle.native` 已弃用，不需要使用。

## 燃料

- 上限：普通海龟 20,000，高级海龟 100,000（服务器可配；配置关闭燃料时 `getFuelLevel()` 返回 `"unlimited"`）。
- 任何熔炉燃料都能用。常用值：煤/木炭 80，煤块 800，岩浆桶 1000（= 熔炉燃烧时间（刻）÷ 20；1 燃料 = 移动 1 格）。
- `refuel()` 会一直消耗当前槽物品直到加满或用完；只想用一部分写 `refuel(数量)`。

```lua
local function ensure_fuel(min)
    local level = turtle.getFuelLevel()
    if level == "unlimited" or level >= min then return true end
    for slot = 1, 16 do
        turtle.select(slot)
        if turtle.refuel(0) then
            turtle.refuel()
            if turtle.getFuelLevel() >= min then return true end
        end
    end
    turtle.select(1)
    return turtle.getFuelLevel() >= min
end

if not ensure_fuel(200) then error("燃料不足，请放入煤炭", 0) end
```

## 工具与升级

- 任何**钻石工具**都可作为升级：镐（挖任意生存可破坏的原版方块）、斧、铲、锄、剑（攻击；`turtle_sword_harvestable` 标签方块）。数据包可增加更多。
- 外设升级：无线/末影调制解调器、扬声器 → 以 `"left"`/`"right"` 外设访问（如 `rednet.open("left")`）。
- 工作台 → 启用 `turtle.craft`。
- 所有工具都能破坏瞬间破坏的方块（树苗等）；`computercraft:always_breakable` 标签另加树叶、竹子等。
- 装备：合成时把海龟和升级一起合成，或运行中用 `equipLeft/Right`。

## 可靠的移动与挖掘封装

```lua
-- 前进：遇到方块就挖，遇到生物就攻击；沙砾落下会重复挖
local function forward()
    for _ = 1, 30 do
        if turtle.forward() then return true end
        if turtle.detect() then
            if not turtle.dig() then return false, "无法挖掉前方方块" end
        else
            turtle.attack()
        end
    end
    return false, "前进失败（燃料或阻挡）"
end

local function up()
    for _ = 1, 30 do
        if turtle.up() then return true end
        if turtle.detectUp() then
            if not turtle.digUp() then return false, "无法挖掉上方方块" end
        else
            turtle.attackUp()
        end
    end
    return false, "上升失败"
end

local function down()
    for _ = 1, 30 do
        if turtle.down() then return true end
        if turtle.detectDown() then
            if not turtle.digDown() then return false, "无法挖掉下方方块" end
        else
            turtle.attackDown()
        end
    end
    return false, "下降失败"
end

local ok, err = forward()
if not ok then printError(err) end
```

要点：
- 用次数上限而不是无限 `while`，避免基岩/保护区域卡死。
- 失败原因可能来自燃料：先 `ensure_fuel`。
- 挖头顶时沙砾会持续落下：`while turtle.detectUp() do turtle.digUp() end`。

## 坐标与朝向跟踪

海龟没有内置坐标。两种方案：

1. **相对坐标**：从起点 (0,0,0)、朝向 0 开始，在每次**成功**移动/转向后更新。
2. **GPS**：`gps.locate()` 得到绝对坐标（需要 GPS 星座和无线调制解调器）；朝向可通过前进一格前后两次定位推算。

```lua
-- 朝向：0=前(+z 方向假设)，1=右，2=后，3=左；按自己约定即可
local pos = { x = 0, y = 0, z = 0, dir = 0 }
local DX = { [0] = 0, 1, 0, -1 }
local DZ = { [0] = 1, 0, -1, 0 }

local function turn_right()
    turtle.turnRight()
    pos.dir = (pos.dir + 1) % 4
end

local function turn_left()
    turtle.turnLeft()
    pos.dir = (pos.dir + 3) % 4
end

local function step_forward()
    if turtle.forward() then
        pos.x, pos.z = pos.x + DX[pos.dir], pos.z + DZ[pos.dir]
        return true
    end
    return false
end

local function face(dir)
    while pos.dir ~= dir do turn_right() end
end

turn_left()
step_forward()
face(0)
print(pos.x, pos.y, pos.z, pos.dir)
```

需要断电后继续时，把 `pos` 用 `textutils.serialise` 写入文件，每步更新（注意移动成功后、写文件前断电会差一格——关键任务用 GPS 校正）。

## 物品栏管理

```lua
-- 背包是否满（留出 keep 个空槽）
local function is_full(keep)
    local empty = 0
    for slot = 1, 16 do
        if turtle.getItemCount(slot) == 0 then empty = empty + 1 end
    end
    return empty <= (keep or 0)
end

-- 把除燃料外的所有物品放进前方箱子
local function unload()
    for slot = 1, 16 do
        turtle.select(slot)
        if turtle.getItemCount(slot) > 0 and not turtle.refuel(0) then
            turtle.drop()
        end
    end
    turtle.select(1)
end

-- 找到某物品所在槽
local function find_item(name)
    for slot = 1, 16 do
        local item = turtle.getItemDetail(slot)
        if item and item.name == name then return slot end
    end
    return nil
end
```

- 丢弃垃圾方块：检查 `item.name` 是否在垃圾表中再 `drop`。
- 按标签判断（如所有原木）：`turtle.getItemDetail(slot, true)` 的 `tags["minecraft:logs"]`。

## 常见任务要点

| 任务 | 要点 |
|---|---|
| 隧道 / 矿道 | 每格 `dig` 前方 + `digUp`（+ `digDown`）；处理沙砾；定期 `is_full` 返回卸货；计算回程燃料（距离 × 1 + 余量） |
| 挖掘区域（quarry） | 蛇形逐层；层间 `digDown` + `down`；保存进度；遇基岩 `dig` 返回 false 时结束 |
| 砍树 | `inspect` 判断 `tags["minecraft:logs"]`；向上挖到顶再下来；补种树苗用 `place` |
| 种田 | `inspectDown` 读作物 `state.age`（小麦成熟为 7）；`digDown` 收割后 `placeDown` 播种；锄头可耕地 |
| 建造 | 放置前 `select` 到有方块的槽；方块用完要换槽（`find_item`）；`place` 返回 false 说明前方有东西或无可放物 |
| 合成 | 只能在海龟物品栏内摆配方；先把无关物品丢进箱子 |
| 与箱子交互 | `suck`/`drop` 只作用于正前/上/下方；海龟不能用 `pushItems`，除非 1.121.0+ 装备了存储物品（`turtle_storage`） |
| 自带的程序 | ROM 里有 `excavate`、`tunnel`、`go`、`refuel`、`dance` 等（`programs` 查看），可先用它们验证环境 |

## 区块加载与断点续跑

- 海龟所在区块被卸载（如玩家走远）时海龟停止运行，海龟也不能移动进未加载的区块；区块重新加载时计算机重新开机——**内存里的变量全部丢失**，只会再跑一次启动文件。
- 长任务：用 `startup.lua` 读取进度文件继续；或使用区块加载器（其他模组）/保持玩家在附近。
- 给海龟起标签（`label set 名字`）方便识别；挖下来的海龟保留文件和燃料。
