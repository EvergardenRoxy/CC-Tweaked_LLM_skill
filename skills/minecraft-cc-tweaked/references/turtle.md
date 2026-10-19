# Turtle programming

[Core](../SKILL.md) · [Recovery](state-and-recovery.md) · [Official turtle API](https://tweaked.cc/module/turtle.html)

## Movement and fuel

Check the result of each move/turn/dig/place/attack operation. A blocked move does not advance the coordinate model. Do not automatically dig or attack whenever movement fails: the obstruction may be protected, valuable, another entity, or outside the user's authorized area.

Fuel may be numeric or `"unlimited"`. Use `refuel(0)` to test a selected stack's suitability, and consume only an explicit amount when refueling is intended. Slot count, upgrades, tool side, and limits should match the installed turtle; avoid copying creative-mode assumptions into survival programs.

```lua
local function move_forward_once()
    local ok, reason = turtle.forward()
    if not ok then return false, reason end
    return true
end
return move_forward_once
```

This helper deliberately does not retry or update a navigation ledger. Consequential autonomous navigation needs a pose model, allowed region, resource budget, stop policy, and interruption handling.

## Pose and interruption

GPS may establish position but not facing. Keep dimension, coordinates, and orientation explicit. Update a pose only after confirmed motion. A crash after movement but before saving makes a persisted pose uncertain; re-establish it from a trusted reference or stop. A saved step counter does not make navigation exactly once.

Give retries a maximum count/time and a reason. Falling blocks, entities, unloaded destinations, fuel shortage, and blocked return paths need different responses. Do not write an unbounded dig-forward loop as a universal recovery mechanism.

## Inventory and tasks

Inspect all relevant slots with actual counts; reserve tools, fuel, seeds, or build materials by explicit policy. Check space before collecting, and actual drop/suck/transfer results before updating totals. A selected slot can change crafting/refueling behavior.

For mining, define a permitted volume and return route. For farming, inspect actual block states and the pack's growth/seed rules. For crafting, confirm the effective recipe and grid arrangement. For building, validate block identity, orientation, replaceability, and remaining materials. Vanilla examples are not assertions about modded recipes or protected-server behavior.

Chunk loading and restart depend on server configuration and installed upgrades. A turtle chunk loader may cover only a configured area; it does not prove an entire factory/return route stays loaded. AP extensions are separate peripheral/plugin methods, not additions automatically available on `turtle.*`.
