# Peripheral discovery and core capabilities

[Core](../SKILL.md) · [Official peripheral API](https://tweaked.cc/module/peripheral.html)

## Bind the intended device

A directly attached device can be addressed by side. Remote wired devices use their actual network names. Enable the wired modem connections and verify visibility; a guessed block name is not a network name.

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

Store a chosen name and role in configuration. Recheck presence, types, and required methods at startup and after `peripheral`/`peripheral_detach` events. A wrapper can fail after a successful presence check; protect calls where disappearance is recoverable.

`peripheral.find` can return several results. It is convenient for a genuinely unique optional device; using its first result is unsafe when the choice controls physical equipment. A custom mod display name may not be the wired network name.

## Generic handlers

| Type | Methods | Semantics |
|---|---|---|
| `inventory` | `size`, `list`, `getItemDetail`, `getItemLimit`, `pushItems`, `pullItems` where supported | `list` is sparse; transfers return actual moved count |
| `fluid_storage` | `tanks`, `pushFluid`, `pullFluid` | Tank tables may be sparse; confirm resource identity and units |
| `energy_storage` | `getEnergy`, `getEnergyCapacity` | Stored energy/capacity differ from transfer rate; confirm units |

Transfers use a destination/source **network name string**, not a wrapped object. Slot numbers are one-based for core inventory methods. Specialized machine handlers may expose different input/output access or reject some slots.

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

This groups by item ID only. Include relevant components/fingerprint when distinct variants must remain separate. Read details only for selected slots; field availability and NBT/component representation change with versions and handlers.

For a move, validate source, destination, item predicate, and requested limit. A returned zero means no movement; a partial count means partial movement. An exception can leave completion uncertain. Read back the affected locations before a consequential retry; see [recovery](state-and-recovery.md).

## Other core devices

| Device | Use | Checks |
|---|---|---|
| `monitor` | Terminal-like rendering, advanced touch | `getSize` columns then rows; scale/resize and source name |
| `speaker` | Notes, sounds, audio | `playAudio` false means backpressure; wait for the matching speaker's `speaker_audio_empty` |
| `modem` | Wired/wireless messages | Channel limits, wired visibility, wireless/dimension constraints |
| `printer` | Page lifecycle and text | Paper/ink, successful page creation, printable dimensions, page completion |
| `drive` | Data/audio media | Present media, mount path, read-only state |
| `computer` | Adjacent/network computer control | `turnOn`, `shutdown`, `reboot` change another computer's state |
| `redstone_relay` | Remote redstone | Version support, physical side, event payload/source |

Generic handler support is conditional on the runtime and block implementation. A Create machine without a specialized API may still expose inventory or fluid access. Capability discovery does not establish a crafting/progress API.

## Observation quality

Aggregate the full data before returning a compact summary to a tool. A preview marked as truncated cannot support full inventory totals. Preserve sampling scope, time, item identity, and omissions. Reads across several containers are not an atomic snapshot; players and machines can move items during sampling.
