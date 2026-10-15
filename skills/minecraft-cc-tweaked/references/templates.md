# 程序模板库

> 每个模板都是完整程序，已用 Lua 5.2 编译器做语法检查，并核对了 tweaked.cc 上的 API 名称。使用前按"安装"一栏摆放设备，并把文件顶部的配置常量改成用户实际的外设名。

## 目录

1. 仓库物品统计显示器
2. 自动熔炉阵列（有线网络）
3. 物品分拣（按名字/标签分流，溢出箱）
4. 海龟伐木
5. 海龟隧道（带返回与卸货）
6. 海龟小麦农场
7. rednet 远程红石开关（服务端 + 客户端）
8. 显示器触摸按钮面板
9. 能量监控 + 发电机自动启停
10. 储罐液位显示
11. 密码门
12. 扬声器播放网络上的 DFPWM 音频
13. 断点续跑的启动包装
14. 多扬声器同步播放器（暂停、跳转、音量、热插拔）

---

## 1. 仓库物品统计显示器

**安装**：高级计算机；显示器任意尺寸（贴在计算机或联网）；所有箱子用有线调制解调器联网并右键启用。

```lua
-- storage_monitor.lua：统计所有 inventory 外设里的物品，按数量排序显示
local REFRESH = 10            -- 秒
local BATCH = 32              -- 每批并发扫描的箱子数

local mon = peripheral.find("monitor") or error("没有显示器", 0)
mon.setTextScale(0.5)

local function scan()
    local invs = { peripheral.find("inventory") }
    local totals = {}
    for start = 1, #invs, BATCH do
        local tasks = {}
        for i = start, math.min(start + BATCH - 1, #invs) do
            local inv = invs[i]
            tasks[#tasks + 1] = function()
                for _, item in pairs(inv.list()) do
                    totals[item.name] = (totals[item.name] or 0) + item.count
                end
            end
        end
        parallel.waitForAll(table.unpack(tasks))
    end
    local list = {}
    for name, count in pairs(totals) do
        list[#list + 1] = { name = name, count = count }
    end
    table.sort(list, function(a, b) return a.count > b.count end)
    return list, #invs
end

local function draw(list, n)
    local w, h = mon.getSize()
    mon.setBackgroundColour(colours.black)
    mon.clear()
    mon.setCursorPos(1, 1)
    mon.setTextColour(colours.yellow)
    mon.write(("Storage: %d inventories, %d kinds"):format(n, #list))
    mon.setTextColour(colours.white)
    for i = 1, math.min(#list, h - 1) do
        local e = list[i]
        local short = e.name:gsub("^minecraft:", "")
        local count = tostring(e.count)
        mon.setCursorPos(1, i + 1)
        mon.write(short:sub(1, w - #count - 1))
        mon.setCursorPos(w - #count + 1, i + 1)
        mon.write(count)
    end
end

while true do
    local list, n = scan()
    draw(list, n)
    sleep(REFRESH)
end
```

## 2. 自动熔炉阵列（有线网络）

**安装**：计算机 + 有线网络连接：一个输入箱（矿石）、一个燃料箱、一个输出箱、若干原版熔炉（`minecraft:furnace`）。熔炉槽位：1 = 原料，2 = 燃料，3 = 产物。

```lua
-- furnaces.lua
local INPUT = "minecraft:chest_0"    -- 改成实际名字
local FUEL = "minecraft:chest_1"
local OUTPUT = "minecraft:chest_2"
local PER_FURNACE = 8                 -- 每台熔炉补到多少个原料
local INTERVAL = 5

local input = peripheral.wrap(INPUT) or error("找不到输入箱 " .. INPUT, 0)
local fuel = peripheral.wrap(FUEL) or error("找不到燃料箱 " .. FUEL, 0)
local output = peripheral.wrap(OUTPUT) or error("找不到输出箱 " .. OUTPUT, 0)
local furnaces = { peripheral.find("minecraft:furnace") }
if #furnaces == 0 then error("网络上没有熔炉", 0) end

local function first_slot(inv)
    for slot, item in pairs(inv.list()) do
        return slot, item
    end
end

local function service(furnace)
    local name = peripheral.getName(furnace)
    local items = furnace.list()
    -- 取出产物
    if items[3] then output.pullItems(name, 3) end
    -- 补原料
    local have = items[1] and items[1].count or 0
    if have < PER_FURNACE then
        local slot = first_slot(input)
        if slot then input.pushItems(name, slot, PER_FURNACE - have, 1) end
    end
    -- 补燃料
    if not items[2] or items[2].count < 4 then
        local slot = first_slot(fuel)
        if slot then fuel.pushItems(name, slot, 8, 2) end
    end
end

print(("管理 %d 台熔炉，Ctrl+T 停止"):format(#furnaces))
while true do
    local tasks = {}
    for _, f in ipairs(furnaces) do
        tasks[#tasks + 1] = function() service(f) end
    end
    parallel.waitForAll(table.unpack(tasks))
    sleep(INTERVAL)
end
```

要点：熔炉的原料槽一次只放一种物品，若输入箱混放多种矿石，`pushItems` 到已有其他物品的槽会返回 0（不报错）；需要分种类时按 `items[1].name` 匹配后再推。

## 3. 物品分拣（按名字/标签分流，溢出箱）

**安装**：有线网络：输入箱、各目标箱、溢出箱。

```lua
-- sorter.lua
local INPUT = "minecraft:chest_0"
local OVERFLOW = "minecraft:chest_9"
-- 规则从上到下匹配：name 精确匹配，或 tag 匹配（需要 getItemDetail）
local RULES = {
    { name = "minecraft:cobblestone", to = "minecraft:chest_1" },
    { tag = "minecraft:logs", to = "minecraft:chest_2" },
    { tag = "c:ores", to = "minecraft:chest_3" },
}

local input = peripheral.wrap(INPUT) or error("找不到输入箱", 0)
local tag_cache = {}

local function tags_of(slot, item)
    local key = item.name .. "|" .. (item.nbt or "")
    if not tag_cache[key] then
        local detail = input.getItemDetail(slot)
        tag_cache[key] = detail and detail.tags or {}
    end
    return tag_cache[key]
end

local function target_for(slot, item)
    for _, rule in ipairs(RULES) do
        if rule.name and rule.name == item.name then return rule.to end
        if rule.tag and tags_of(slot, item)[rule.tag] then return rule.to end
    end
    return OVERFLOW
end

while true do
    for slot, item in pairs(input.list()) do
        local to = target_for(slot, item)
        local moved = input.pushItems(to, slot)
        if moved < item.count and to ~= OVERFLOW then
            input.pushItems(OVERFLOW, slot)        -- 目标满了就进溢出箱
        end
    end
    sleep(2)
end
```

标签名随整合包/版本不同（如 `c:ores` 与 `forge:ores`），让用户用 `getItemDetail` 查看实际标签。

## 4. 海龟伐木

**安装**：伐木海龟（钻石斧或镐），面前一格种树苗位置；槽 1 放树苗，槽 16 放燃料；海龟**后方**放箱子收木头。适用于 1×1 的树（橡树、白桦等）。

```lua
-- lumberjack.lua
local SAPLING_SLOT, FUEL_SLOT = 1, 16

local function refuel()
    local level = turtle.getFuelLevel()
    if level ~= "unlimited" and level < 100 then
        turtle.select(FUEL_SLOT)
        turtle.refuel(4)
        turtle.select(SAPLING_SLOT)
    end
end

local function is_log(data)
    return data.tags and data.tags["minecraft:logs"]
end

local function chop()
    turtle.dig()
    if not turtle.forward() then return end
    local height = 0
    while true do
        local ok, data = turtle.inspectUp()
        if not (ok and is_log(data)) then break end
        turtle.digUp()
        if not turtle.up() then break end
        height = height + 1
    end
    for _ = 1, height do
        while not turtle.down() do turtle.digDown() end
    end
    turtle.back()
end

local function unload()
    turtle.turnLeft()
    turtle.turnLeft()
    for slot = 2, 15 do
        turtle.select(slot)
        turtle.drop()
    end
    turtle.turnRight()
    turtle.turnRight()
    turtle.select(SAPLING_SLOT)
end

turtle.select(SAPLING_SLOT)
while true do
    refuel()
    local ok, data = turtle.inspect()
    if ok and is_log(data) then
        chop()
        unload()
    end
    if not turtle.detect() and turtle.getItemCount(SAPLING_SLOT) > 1 then
        turtle.place()
    end
    turtle.suck()            -- 捡起前方掉落的树苗
    sleep(30)
end
```

## 5. 海龟隧道（带返回与卸货）

**安装**：挖掘海龟；起点**后方**放箱子；运行 `tunnel2 50` 挖 1×2、长 50 的隧道。

```lua
-- tunnel2.lua
local length = tonumber((...)) or error("用法: tunnel2 <长度>", 0)

local function fuel_ok(need)
    local level = turtle.getFuelLevel()
    return level == "unlimited" or level >= need
end

local function refuel_all()
    for slot = 1, 16 do
        turtle.select(slot)
        if turtle.refuel(0) then turtle.refuel() end
    end
    turtle.select(1)
end

local function dig_forward()
    for _ = 1, 30 do
        if turtle.forward() then return true end
        if turtle.detect() then turtle.dig() else turtle.attack() end
    end
    return false
end

local function full()
    for slot = 1, 16 do
        if turtle.getItemCount(slot) == 0 then return false end
    end
    return true
end

local function go_back(steps)
    turtle.turnLeft()
    turtle.turnLeft()
    for _ = 1, steps do
        while not turtle.forward() do
            if turtle.detect() then turtle.dig() else turtle.attack() end
        end
    end
end

local function unload()
    for slot = 1, 16 do
        turtle.select(slot)
        if not turtle.refuel(0) then turtle.drop() end
    end
    turtle.select(1)
end

refuel_all()
if not fuel_ok(length * 2 + 10) then
    error(("燃料不足：需要约 %d"):format(length * 2 + 10), 0)
end

local dug = 0
while dug < length do
    if not dig_forward() then
        printError("前方无法通过，停止")
        break
    end
    dug = dug + 1
    while turtle.detectUp() do turtle.digUp() end
    if full() then
        go_back(dug)
        unload()
        turtle.turnLeft()
        turtle.turnLeft()
        for _ = 1, dug do assert(dig_forward(), "返回挖掘点失败") end
    end
end

go_back(dug)
unload()
turtle.turnLeft()
turtle.turnLeft()
print("完成，挖了 " .. dug .. " 格")
```

燃料检查只计算了单程往返（`长度 × 2`）；背包满时中途回去卸货还会多耗燃料，长隧道请多备燃料或在起点箱子旁补充。

## 6. 海龟小麦农场

**安装**：一排已耕好、已灌溉的耕地；海龟（任意工具都能破坏成熟小麦）悬在**作物层上方一格**（耕地 y、作物 y+1、海龟 y+2），起点位于这排耕地之前一格，朝向农田；起点**正下方**放箱子收小麦；槽 1 放种子。海龟收割时掉落物直接进入自身物品栏。

```lua
-- farm.lua：沿直线往返收割成熟小麦并补种
local LENGTH = 9            -- 农田长度
local WAIT = 300            -- 每轮间隔秒数

local function tend()
    local ok, data = turtle.inspectDown()
    if ok and data.name == "minecraft:wheat" and data.state.age == 7 then
        turtle.digDown()
        turtle.select(1)
        turtle.placeDown()   -- 补种
    elseif not ok then
        turtle.select(1)
        turtle.placeDown()   -- 空位直接播种
    end
end

local function deposit()
    for slot = 2, 16 do
        local item = turtle.getItemDetail(slot)
        if item and item.name == "minecraft:wheat" then
            turtle.select(slot)
            turtle.dropDown()
        end
    end
    turtle.select(1)
end

while true do
    local level = turtle.getFuelLevel()
    if level ~= "unlimited" and level < LENGTH * 2 then
        error("燃料不足", 0)
    end
    for _ = 1, LENGTH do
        assert(turtle.forward())
        tend()
    end
    turtle.turnLeft()
    turtle.turnLeft()
    for _ = 1, LENGTH do assert(turtle.forward()) end
    turtle.turnLeft()
    turtle.turnLeft()
    deposit()
    sleep(WAIT)
end
```

## 7. rednet 远程红石开关

**安装**：两台计算机各装无线（或末影）调制解调器。服务端背面接要控制的红石。

```lua
-- switch_server.lua（设为 startup.lua 可开机自启）
local SIDE = "back"
local PROTOCOL = "rs_switch"

peripheral.find("modem", rednet.open)
if not rednet.isOpen() then error("没有调制解调器", 0) end
rednet.host(PROTOCOL, "switch_" .. os.getComputerID())
print("等待命令，ID =", os.getComputerID())

while true do
    local id, msg = rednet.receive(PROTOCOL)
    if msg == "on" then
        redstone.setOutput(SIDE, true)
    elseif msg == "off" then
        redstone.setOutput(SIDE, false)
    elseif msg == "toggle" then
        redstone.setOutput(SIDE, not redstone.getOutput(SIDE))
    end
    rednet.send(id, { state = redstone.getOutput(SIDE) }, PROTOCOL)
end
```

```lua
-- switch.lua：用法 switch <on|off|toggle>
local PROTOCOL = "rs_switch"
local cmd = ...
if cmd ~= "on" and cmd ~= "off" and cmd ~= "toggle" then
    error("用法: switch <on|off|toggle>", 0)
end

peripheral.find("modem", rednet.open)
local servers = { rednet.lookup(PROTOCOL) }
if #servers == 0 then error("找不到开关服务端", 0) end

for _, server in ipairs(servers) do
    rednet.send(server, cmd, PROTOCOL)
    local id, reply = rednet.receive(PROTOCOL, 3)
    if id and type(reply) == "table" then
        print(("#%d -> %s"):format(id, reply.state and "ON" or "OFF"))
    else
        printError(("#%d 无响应"):format(server))
    end
end
```

## 8. 显示器触摸按钮面板

**安装**：高级计算机 + **高级显示器**（至少 2×2）；继电器或计算机各面接设备。

```lua
-- panel.lua
local mon = peripheral.find("monitor") or error("没有显示器", 0)
if not mon.isColour() then error("需要高级显示器", 0) end
mon.setTextScale(1)

local buttons = {
    { label = "Lights", side = "left", y = 2 },
    { label = "Pump", side = "right", y = 4 },
    { label = "Door", side = "top", y = 6 },
}

local function draw()
    local w = mon.getSize()
    mon.setBackgroundColour(colours.black)
    mon.clear()
    for _, b in ipairs(buttons) do
        local on = redstone.getOutput(b.side)
        mon.setBackgroundColour(on and colours.green or colours.red)
        mon.setTextColour(colours.white)
        mon.setCursorPos(2, b.y)
        local text = (" %s: %s "):format(b.label, on and "ON" or "OFF")
        mon.write(text .. string.rep(" ", math.max(0, w - 2 - #text)))
    end
    mon.setBackgroundColour(colours.black)
end

draw()
while true do
    local event, name, x, y = os.pullEvent()
    if event == "monitor_touch" and name == peripheral.getName(mon) then
        for _, b in ipairs(buttons) do
            if y == b.y then
                redstone.setOutput(b.side, not redstone.getOutput(b.side))
            end
        end
        draw()
    elseif event == "monitor_resize" then
        draw()
    end
end
```

## 9. 能量监控 + 发电机自动启停

**安装**：计算机通过有线网络或相邻连接一个能量存储方块（提供 `energy_storage`）；计算机 `back` 面红石接发电机的"开启"信号（多数发电机红石信号 = 运行或停止，按机器设置调整 `ON_SIGNAL`）。

```lua
-- energy.lua：低于 20% 开机，高于 90% 停机（迟滞，避免频繁开关）
local SIDE = "back"
local LOW, HIGH = 0.20, 0.90
local ON_SIGNAL = true
local INTERVAL = 2

local cell = peripheral.find("energy_storage") or error("没有能量存储外设", 0)
local mon = peripheral.find("monitor")
local running = redstone.getOutput(SIDE) == ON_SIGNAL
local last_energy, last_time = cell.getEnergy(), os.clock()

while true do
    sleep(INTERVAL)
    local energy, cap = cell.getEnergy(), cell.getEnergyCapacity()
    local now = os.clock()
    local rate = (energy - last_energy) / ((now - last_time) * 20)   -- FE/刻
    last_energy, last_time = energy, now
    local ratio = cap > 0 and energy / cap or 0

    if ratio < LOW then running = true elseif ratio > HIGH then running = false end
    redstone.setOutput(SIDE, running == ON_SIGNAL)

    local line1 = ("Energy %5.1f%%  %s"):format(ratio * 100, running and "GEN ON" or "GEN OFF")
    local line2 = ("Rate %+.0f FE/t"):format(rate)
    if mon then
        mon.clear()
        mon.setCursorPos(1, 1)
        mon.write(line1)
        mon.setCursorPos(1, 2)
        mon.write(line2)
    else
        term.clear()
        term.setCursorPos(1, 1)
        print(line1)
        print(line2)
    end
end
```

## 10. 储罐液位显示

**安装**：高级显示器 + 若干提供 `fluid_storage` 的储罐（有线网络）。

```lua
-- tanks.lua
local mon = peripheral.find("monitor") or error("没有显示器", 0)
mon.setTextScale(0.5)

local function bar(y, label, ratio, colour)
    local w = mon.getSize()
    local width = w - 2
    local filled = math.floor(width * ratio + 0.5)
    mon.setCursorPos(1, y)
    mon.setBackgroundColour(colours.black)
    mon.setTextColour(colours.white)
    mon.write(label:sub(1, w))
    mon.setCursorPos(2, y + 1)
    mon.setBackgroundColour(colour)
    mon.write(string.rep(" ", filled))
    mon.setBackgroundColour(colours.grey)
    mon.write(string.rep(" ", width - filled))
end

while true do
    mon.setBackgroundColour(colours.black)
    mon.clear()
    local y = 1
    for _, tank in ipairs({ peripheral.find("fluid_storage") }) do
        local name = peripheral.getName(tank)
        for _, fluid in pairs(tank.tanks()) do
            local label = ("%s %s: %d mB"):format(name, fluid.name, fluid.amount)
            -- tanks() 不提供容量；这里以 64000 mB 为满，按实际储罐修改
            bar(y, label, math.min(1, fluid.amount / 64000), colours.blue)
            y = y + 3
        end
    end
    sleep(5)
end
```

`tanks()` 只返回 `name` 与 `amount`，不含容量；容量需要用户告知或查看模组外设的专有方法（`peripheral.getMethods`）。

## 11. 密码门

**安装**：计算机，`front` 面接铁门（或活塞门）。保存为 `startup.lua`。

```lua
-- startup.lua
local PASSWORD = "change-me"
local SIDE = "front"
local OPEN_TIME = 3

os.pullEvent = os.pullEventRaw      -- 禁止 Ctrl+T 终止

while true do
    term.clear()
    term.setCursorPos(1, 1)
    write("Password: ")
    local input = read("*")
    if input == PASSWORD then
        print("Welcome")
        redstone.setOutput(SIDE, true)
        sleep(OPEN_TIME)
        redstone.setOutput(SIDE, false)
    else
        print("Wrong password")
        sleep(2)
    end
end
```

风险：覆盖 `os.pullEvent` 后程序无法用 Ctrl+T 停止；修改程序需要从磁盘驱动器启动（软盘里放一个空的 `startup.lua`），或在测试阶段先注释掉那一行。密码以明文存在文件里，能接触计算机的人都能读到。

## 12. 扬声器播放网络上的 DFPWM 音频

**安装**：计算机 + 扬声器；服务器允许 HTTP 访问该网址。用法：`play <url>`。

```lua
-- play.lua
local url = ... or error("用法: play <dfpwm 文件网址>", 0)
local dfpwm = require("cc.audio.dfpwm")
local speaker = peripheral.find("speaker") or error("没有扬声器", 0)

local res, err = http.get(url, nil, true)       -- 二进制模式
if not res then error("下载失败: " .. tostring(err), 0) end

local decoder = dfpwm.make_decoder()
while true do
    local chunk = res.read(16 * 1024)
    if not chunk or #chunk == 0 then break end
    local buffer = decoder(chunk)
    while not speaker.playAudio(buffer) do
        os.pullEvent("speaker_audio_empty")
    end
end
res.close()
```

要点：二进制模式下载；每块 16 KiB 的 DFPWM 正好解码成 131072 个样本（扬声器单次上限 128×1024）；`playAudio` 返回 false 时等 `speaker_audio_empty` 再重试**同一块**。超过服务器下载上限（默认约 16 MiB）的文件要用 Range 分段下载（见 `app-engineering.md`）。

## 13. 断点续跑的启动包装

把长任务的进度写入文件，区块重载/重启后从 `startup.lua` 继续。

```lua
-- startup.lua
local STATE_FILE = "/job_state"
local TOTAL = 100

local function load_state()
    if not fs.exists(STATE_FILE) then return { step = 0 } end
    local h = fs.open(STATE_FILE, "r")
    local data = textutils.unserialise(h.readAll())
    h.close()
    return data or { step = 0 }
end

local function save_state(state)
    local h = fs.open(STATE_FILE, "w")
    h.write(textutils.serialise(state))
    h.close()
end

local function do_step(n)
    print("working on step", n)
    sleep(1)                                -- 换成实际工作
end

local state = load_state()
while state.step < TOTAL do
    do_step(state.step + 1)
    state.step = state.step + 1
    save_state(state)
end
fs.delete(STATE_FILE)
print("job finished")
```

## 14. 多扬声器同步播放器（暂停、跳转、音量、热插拔）

**安装**：计算机 + 一个或多个扬声器（相邻或有线网络）；DFPWM 文件放在本机。用法：`player /music/song.dfpwm`。按键：空格 暂停/继续，←/→ 后退/前进 10 秒，↑/↓ 音量，Q 退出。

DFPWM 基本事实：48 kHz、每个样本 1 bit，所以 **1 秒 = 6000 字节**；时长 = 文件字节数 ÷ 6000，跳转 = 改变字节偏移。解码器有内部状态：同一条音频流用一个解码器（解一次、发给所有扬声器）；跳转后换新解码器，避免接缝处杂音；不同的流（如左右声道各一个文件）各用各的解码器。

```lua
-- player.lua
local path = ... or error("用法: player <文件.dfpwm>", 0)
local dfpwm = require("cc.audio.dfpwm")

local BYTES_PER_SECOND = 6000
local CHUNK = 16 * 1024                 -- 每块约 2.7 秒

local h = fs.open(path, "rb") or error("无法打开 " .. path, 0)
local data = h.readAll()
h.close()

local state = { offset = 0, paused = false, volume = 1, decoder = dfpwm.make_decoder() }

local function speakers()
    local list = {}
    for _, name in ipairs(peripheral.getNames()) do
        if peripheral.hasType(name, "speaker") then list[#list + 1] = peripheral.wrap(name) end
    end
    return list
end

local function seek(seconds)
    local target = state.offset + seconds * BYTES_PER_SECOND
    state.offset = math.max(0, math.min(#data, math.floor(target)))
    state.decoder = dfpwm.make_decoder()          -- 跳转后重置解码器
    for _, sp in ipairs(speakers()) do pcall(sp.stop) end
end

local function status()
    local x, y = term.getCursorPos()
    term.setCursorPos(1, y)
    term.clearLine()
    write(("%s %3d/%3ds vol %.1f"):format(state.paused and "||" or "> ",
        math.floor(state.offset / BYTES_PER_SECOND), math.floor(#data / BYTES_PER_SECOND), state.volume))
    term.setCursorPos(x, y)
end

-- 把一块音频送进所有扬声器；只对拒收的扬声器重试，全部接受后才前进
local function play_loop()
    while state.offset < #data do
        if state.paused then
            os.pullEvent("player_resume")
        else
            local pending = speakers()
            if #pending == 0 then
                status()
                os.pullEvent("peripheral")                 -- 没有扬声器：等接入后重试这一块
            else
                local chunk = data:sub(state.offset + 1, state.offset + CHUNK)
                local offset_at_start = state.offset
                local buffer = state.decoder(chunk)
                while #pending > 0 and state.offset == offset_at_start and not state.paused do
                    local retry = {}
                    for _, sp in ipairs(pending) do
                        local ok, accepted = pcall(sp.playAudio, buffer, state.volume)
                        if ok and not accepted then retry[#retry + 1] = sp end   -- ok=false：已断开，丢弃
                    end
                    pending = retry
                    if #pending > 0 then os.pullEvent("speaker_audio_empty") end
                end
                if state.offset == offset_at_start and not state.paused then
                    state.offset = state.offset + #chunk
                end
                status()
            end
        end
    end
end

local function key_loop()
    while true do
        local _, key = os.pullEvent("key")
        if key == keys.space then
            state.paused = not state.paused
            if state.paused then
                for _, sp in ipairs(speakers()) do pcall(sp.stop) end
                state.decoder = dfpwm.make_decoder()      -- 继续时从当前块重新解码
            else
                os.queueEvent("player_resume")
            end
        elseif key == keys.left then seek(-10)
        elseif key == keys.right then seek(10)
        elseif key == keys.up then state.volume = math.min(3, state.volume + 0.5)
        elseif key == keys.down then state.volume = math.max(0, state.volume - 0.5)
        elseif key == keys.q then return
        end
        status()
    end
end

print(("播放 %s，时长 %d 秒"):format(path, math.floor(#data / BYTES_PER_SECOND)))
print("空格 暂停  ←/→ 跳转  ↑/↓ 音量  Q 退出")
status()
parallel.waitForAny(play_loop, key_loop)
for _, sp in ipairs(speakers()) do pcall(sp.stop) end
print()
print("结束")
```

要点：
- 所有扬声器写入**同一块**解码结果，只有全部接受后才读下一块，多台扬声器保持同步；新接入的扬声器从下一块开始加入。
- `pcall` 包住 `playAudio`：外设在播放中被拆掉时只丢弃该扬声器，不中断播放。
- 暂停用 `speaker.stop()` 清空缓冲，否则还会播完已缓冲的约几秒音频。
- 整个文件读入内存：文件很大（几十 MB）时改为按块 `h.read(CHUNK)` 流式读取。
