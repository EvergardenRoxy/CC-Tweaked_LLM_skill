# Peripheral discovery and core capabilities

[Core](../SKILL.md) · [Official peripheral API](https://tweaked.cc/module/peripheral.html)

## Bind the intended device

A device touching the computer is addressed by its side (`top`, `left`, ...). A device on a wired network uses its network name, such as `minecraft:chest_0`. Attach a wired modem to each device, connect them with cable, and right-click each modem to connect it; it shows the name in chat. A guessed block name is not a network name.

```lua
local names = peripheral.getNames()
table.sort(names)
for _, name in ipairs(names) do
    local types = { peripheral.getType(name) }
    local methods = peripheral.getMethods(name) or {}
    table.sort(methods)
    print(name, table.concat(types, ","), table.concat(methods, ","))
end
```

Store the chosen name and its role in configuration. Recheck presence, types, and required methods at startup and after `peripheral`/`peripheral_detach` events. A device can disappear right after a successful check, so wrap calls in `pcall` where the program should survive that.

`peripheral.find` returns every match. Taking the first is fine when exactly one such device exists, but unsafe when the choice controls machinery. A display name set in a mod is not the network name.

## Generic handlers

| Type | Methods | Semantics |
|---|---|---|
| `inventory` | `size`, `list`, `getItemDetail`, `getItemLimit`, `pushItems`, `pullItems` where supported | `list` is sparse; transfers return the count actually moved |
| `fluid_storage` | `tanks`, `pushFluid`, `pullFluid` | Tank tables may be sparse; amounts are in mB; check the fluid name |
| `energy_storage` | `getEnergy`, `getEnergyCapacity` | Stored amount and capacity (usually FE), not a transfer rate |

Transfers take the other inventory's **network name string**, not a wrapped object, and both inventories must be on the same wired network. Slot numbers start at 1. Machine inventories may only accept some slots or expose only their inputs or outputs.

```lua
local function totals(inv)
    local result = {}
    for _, item in pairs(inv.list()) do
        result[item.name] = (result[item.name] or 0) + item.count
    end
    return result
end
return totals
```

This groups by item ID only. Include components or the `nbt` hash when variants (enchanted, damaged, named) must stay separate. `getItemDetail` is slower, so call it only for the slots you need; its fields change between versions.

Before a move, check the source, destination, item, and limit. A returned zero means nothing moved; a smaller count means a partial move. If the call raises an error, the move may or may not have happened: read the affected inventories back before retrying anything consequential (see [recovery](state-and-recovery.md)).

## Other core devices

| Device | Use | Checks |
|---|---|---|
| `monitor` | Terminal-style drawing; touch on advanced monitors | `getSize` returns columns, rows; text scale; resize; event source name |
| `speaker` | Notes, sounds, audio | `playAudio` returning false means the buffer is full; wait for that speaker's `speaker_audio_empty` and retry |
| `modem` | Wired/wireless messages | Channels 0 to 65535, open-channel limit, range, dimensions |
| `printer` | Printing pages | Paper and ink, `newPage` result, page size, `endPage` result |
| `drive` | Floppies and music discs | Disk present, mount path, read-only state |
| `computer` | Controlling another computer | `turnOn`, `shutdown`, `reboot` affect that computer |
| `redstone_relay` | Redstone at a distance | Requires 1.114.0+; sides are relative to the relay |

Whether a block exposes generic handlers depends on the CC:T version and the block. A mod machine without its own API may still expose `inventory` or `fluid_storage`; that does not give it a crafting or progress API.

## Observation quality

Aggregate the full data before summarizing it; a truncated preview cannot give inventory totals. Note what was sampled, when, and what was left out. Reading several containers is not an atomic snapshot: players and machines can move items while you read.
