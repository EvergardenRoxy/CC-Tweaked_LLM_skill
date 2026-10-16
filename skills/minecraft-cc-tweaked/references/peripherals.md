# 外设：连接、命名与各外设方法

> 来源：tweaked.cc 的 `peripheral` 模块、Peripherals 与 Generic Peripherals 页面、Item/Block details 参考。

## 目录

- 连接方式与命名
- 通用外设：`inventory`、`fluid_storage`、`energy_storage`
- 物品详情 / 方块详情字段
- 显示器 `monitor`
- 调制解调器 `modem`（有线网络部分）
- 扬声器 `speaker`
- 打印机 `printer`
- 磁盘驱动器 `drive`
- 红石继电器 `redstone_relay`
- 计算机 `computer`、命令方块 `command`
- 海龟存储 `turtle_storage`
- 模组外设的通用排查方法

---

## 连接方式与命名

| 方式 | 外设名 | 说明 |
|---|---|---|
| 贴在计算机某一面 | `"top" "bottom" "left" "right" "front" "back"` | 方向相对于**计算机正面**（屏幕那一面是 front）。海龟的升级槽外设叫 `"left"`/`"right"` |
| 有线网络 | `"<类型>_<编号>"`，如 `"minecraft:chest_0"`、`"monitor_3"` | 计算机和外设各贴一个有线调制解调器，网线连通，**右键外设上的调制解调器**启用（变红，聊天栏打印名字）。整块调制解调器（full block）可一次连接周围多个方块 |

- 名字由游戏分配，**不能自己改**；拆掉重连编号可能变化，所以程序里优先 `peripheral.find`，或把名字写在文件顶部的配置常量里让用户改。
- 同一个外设可以有多个类型：箱子同时是 `"minecraft:chest"` 和 `"inventory"`。`peripheral.find("inventory")` 能找到所有物品容器（包括模组机器）。
- 计算机自身贴在有线网络上时，其他计算机可以把它当 `computer` 外设（名字用 `modem.getNameLocal()` 查）。
- 事件：外设接入 `peripheral, 名字`；断开 `peripheral_detach, 名字`。
- 通过有线网络调用和直接相邻调用的方法完全相同；`modem.callRemote(名字, 方法, ...)` 等价于 `peripheral.call`。

**排查名字：** 让用户运行 `peripherals` 程序（列出全部外设）或：

```lua
for _, name in ipairs(peripheral.getNames()) do
    print(name, table.concat({ peripheral.getType(name) }, ", "))
end
```

---

## 通用外设（1.94.0+）

任何实现了对应能力的方块（原版、模组机器）都会自动获得这些方法，类型名分别是 `inventory`、`fluid_storage`、`energy_storage`。

### `inventory`

| 方法 | 说明 |
|---|---|
| `size()` | 槽位数量 |
| `list()` | `{[槽]={name, count, nbt?}}`，**稀疏表**，用 `pairs` |
| `getItemDetail(槽)` | 详细信息（见下文"物品详情"），空槽 `nil`；槽位越界报错 |
| `getItemLimit(槽)` | 该槽最多放多少（抽屉/桶类可远超 64；1.96.0+） |
| `pushItems(目标名, 源槽 [, 数量 [, 目标槽]])` | 返回实际移动数；目标不存在或不是物品栏时报错 |
| `pullItems(来源名, 源槽 [, 数量 [, 目标槽]])` | 同上，方向相反 |

- 两个容器必须**在同一个有线网络**上，名字用 `peripheral.getName(wrapped)`。
- `nbt` 字段只是哈希值，不包含内容；`name` + `nbt` 相同即为完全相同的物品。
- `list()` 只给基本信息；需要显示名、最大堆叠、标签、耐久时才用 `getItemDetail`（较慢）。
- 每次调用通常需要等一个游戏刻；遍历大量箱子时用 `parallel.waitForAll` 并发（见 `events-and-concurrency.md`）。

```lua
-- 统计网络中所有物品栏的物品总数
local totals = {}
for _, inv in ipairs({ peripheral.find("inventory") }) do
    for _, item in pairs(inv.list()) do
        totals[item.name] = (totals[item.name] or 0) + item.count
    end
end
for name, count in pairs(totals) do print(count, name) end
```

### `fluid_storage`

| 方法 | 说明 |
|---|---|
| `tanks()` | `{[i]={name, amount}}`，**稀疏表**，单位 mB |
| `pushFluid(目标名 [, 上限 [, 流体名]])` | 不给流体名则任选一种；返回移动量 |
| `pullFluid(来源名 [, 上限 [, 流体名]])` | 同上 |

### `energy_storage`

| 方法 | 说明 |
|---|---|
| `getEnergy()` | 当前储能（FE） |
| `getEnergyCapacity()` | 容量（FE） |

能量存储、发电机、耗能机器都可能提供。**无法直接测吞吐量**，需要两次采样相减再除以时间。

---

## 物品详情（`getItemDetail`、`turtle.getItemDetail(槽, true)`）

| 字段 | 说明 |
|---|---|
| `name`、`count`、`nbt?` | 基本信息（`list()` 和非 detailed 的 `turtle.getItemDetail` 只有这些） |
| `displayName` | 显示名（服务器语言） |
| `lore` | 描述行列表 |
| `maxCount` | 最大堆叠 |
| `tags` | `{["minecraft:logs"]=true, ...}`——判断用 `item.tags["minecraft:logs"]` |
| `itemGroups` | 创造物品栏分组（MC 1.19.3–1.20.3 为空） |
| `damage`、`maxDamage`、`durability?`（0–1）、`unbreakable?` | 可损坏物品 |
| `enchantments` | `{ {name, level, displayName}, ... }` |
| `potionEffects` | `{ {name, displayName, duration?, potency?}, ... }`（1.117.0+） |
| `mapColour`/`mapColor` | 地图颜色 RGB 数值（1.117.0+） |

## 方块详情（`turtle.inspect*`、`commands.getBlockInfo`）

| 字段 | 说明 |
|---|---|
| `name` | 方块 ID，如 `"minecraft:wheat"` |
| `state` | 方块状态表，如作物 `{age = 7}`、活塞 `{facing = "up", extended = true}` |
| `tags` | `{["minecraft:logs"]=true, ...}` |
| `mapColour`/`mapColor` | 地图颜色（1.117.0+） |

---

## 显示器 `monitor`

显示器是"终端对象"，拥有 `term` 的全部方法（见 `api-reference.md`），另加：

| 方法 | 说明 |
|---|---|
| `setTextScale(倍数)` | 0.5–5，步长 0.5；越大字越大、可用字符越少 |
| `getTextScale()` | 当前倍数 |

- 多块显示器拼成矩形即合并为一个大屏；尺寸用 `getSize()` 取（随缩放变化），变化时触发 `monitor_resize, 名字`。
- 普通显示器只有灰度；**高级显示器**有颜色，右键触发 `monitor_touch, 名字, x, y`（字符坐标）。
- `mon.write` 不折行；需要 `print` 风格输出时 `term.redirect(mon)`，用完还原。
- 刷新频繁的界面先画到 `window`（隐藏）再一次显示，避免闪烁。

```lua
local mon = peripheral.find("monitor") or error("No monitor attached", 0)
mon.setTextScale(1)
local function center(y, text, fg)
    local w = mon.getSize()
    mon.setCursorPos(math.floor((w - #text) / 2) + 1, y)
    mon.setTextColour(fg or colours.white)
    mon.write(text)
end
mon.setBackgroundColour(colours.black)
mon.clear()
center(1, "Status", colours.yellow)
center(3, "OK", colours.lime)
```

## 调制解调器 `modem`

消息收发见 `networking.md`。有线调制解调器额外提供（无线的没有这些方法，先 `isWireless()` 判断）：

| 方法 | 说明 |
|---|---|
| `getNamesRemote()` | 网络上的外设名（不含本计算机） |
| `isPresentRemote(名)` / `getTypeRemote(名)` / `hasTypeRemote(名, 类型)` / `getMethodsRemote(名)` | 同 `peripheral.*` |
| `callRemote(名, 方法, ...)` | 调用远程外设 |
| `getNameLocal()` | 本计算机在有线网络上的名字 |

## 扬声器 `speaker`

| 方法 | 说明 |
|---|---|
| `playNote(乐器 [, 音量 0–3 [, 音高 0–24]])` | 乐器：`harp basedrum snare hat bass flute bell guitar chime xylophone iron_xylophone cow_bell didgeridoo bit banjo pling`；一刻最多 8 个音符，超出返回 false |
| `playSound(声音名 [, 音量 0–3 [, 速度 0.5–2]])` | 如 `"minecraft:entity.creeper.primed"`；同一时刻只能播一个，失败返回 false |
| `playAudio(样本表 [, 音量])` | 48kHz、-128..127 的 PCM 样本，一次最多 128×1024 个；缓冲满返回 false，等 `speaker_audio_empty` 再试（1.100+） |
| `stop()` | 停止所有声音（1.100+） |

```lua
local dfpwm = require("cc.audio.dfpwm")
local speaker = peripheral.find("speaker") or error("No speaker attached", 0)
local decoder = dfpwm.make_decoder()
for chunk in io.lines("/music.dfpwm", 16 * 1024) do
    local buffer = decoder(chunk)
    while not speaker.playAudio(buffer) do
        os.pullEvent("speaker_audio_empty")
    end
end
```

DFPWM 与多扬声器要点：
- DFPWM 为 48 kHz、每样本 1 bit：**1 秒 = 6000 字节**；16 KiB 一块正好解码出 131072 个样本（`playAudio` 上限）。时长与跳转都按字节换算。
- 解码器有状态：同一条流解码一次、把同一个结果发给所有扬声器；跳转/暂停后新建解码器；不同的流各用一个解码器。
- 多台扬声器同步：同一块写给所有扬声器，只对返回 false 的那几台等待 `speaker_audio_empty` 后重试，全部接受后才送下一块（完整程序见 `templates.md` 第 14 个）。
- 暂停用 `stop()` 清空缓冲；外设可能在播放中被拆掉，`playAudio` 用 `pcall` 包住。
- 音量范围 0–3，不要依赖超出范围时的行为，先用 `math.max(0, math.min(3, v))` 限制。

## 打印机 `printer`

`newPage()`（需要纸和墨，失败返回 false）→ `setPageTitle([标题])`、`setCursorPos(x, y)`、`write(文本)`、`getCursorPos()`、`getPageSize()` → `endPage()`（输出到托盘）；`getInkLevel()`、`getPaperLevel()`。

## 磁盘驱动器 `drive`

`isDiskPresent()`、`hasData()`、`getMountPath()`（如 `"disk"`）、`getDiskLabel()`、`setDiskLabel([标签])`、`getDiskID()`、`hasAudio()`、`getAudioTitle()`、`playAudio()`、`stopAudio()`、`ejectDisk()`。插拔触发 `disk` / `disk_eject` 事件。计算机/海龟放进驱动器也可当磁盘读写其文件。

## 红石继电器 `redstone_relay`（1.114.0+）

方法与 `redstone` API 相同（`setOutput`、`getInput`、`setAnalogOutput`、`getAnalogInput`、`setBundledOutput`……），面名 `top bottom left right front back` 相对继电器。通过有线网络让一台计算机控制很多处红石。输入变化同样触发 `redstone` 事件。

```lua
local relays = { peripheral.find("redstone_relay") }
for _, relay in ipairs(relays) do
    relay.setOutput("top", true)
end
```

## 计算机 `computer`（相邻或联网的其他计算机/海龟）

`turnOn()`、`shutdown()`、`reboot()`、`getID()`、`isOn()`、`getLabel()`。

## 命令方块 `command`

`getCommand()`、`setCommand(命令)`、`runCommand()`（返回 `ok, 错误`）。只有配置项 `enable_command_block` 为 true 时命令方块才会作为外设出现。

## 海龟存储 `turtle_storage`（1.121.0+）

海龟装备潜影盒等存储物品后，作为 `"left"`/`"right"` 外设：`size()`、`list()`、`getItemDetail(槽)`、`pushItems(源槽 [, 数量 [, 海龟槽]])`（盒 → 海龟）、`pullItems([海龟槽 [, 数量 [, 目标槽]]])`（海龟 → 盒）。注意参数**不含外设名**。

---

## 模组外设的通用排查方法

模组方块（Mekanism、AE2、热力、Create、Advanced Peripherals……）可能提供 `inventory` 等通用方法之外的专有方法，名字和参数**各模组各版本都不同**。不要凭记忆写，按以下步骤：

1. `peripheral.getType(名)` 看类型；`peripheral.getMethods(名)` 列出全部方法。
2. 在 `lua` 交互环境中试调用：`p = peripheral.wrap("名")`，`p.方法()`，观察返回值（用 `textutils.serialise` 或 `require("cc.pretty").pretty_print` 打印表）。
3. 把实际可用的方法名告诉 AI 再写程序。
4. 只用通用外设方法（`list`、`pushItems`、`tanks`、`getEnergy`）的程序最可移植。
