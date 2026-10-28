# Turtle programming

[Core](../SKILL.md) · [Recovery](state-and-recovery.md) · [Official turtle API](https://tweaked.cc/module/turtle.html)

## Movement and fuel

Check the result of every move, turn, dig, place, and attack: ordinary action failures return `false, reason`; invalid arguments and other errors may still raise exceptions. Update the position model only after a move succeeds. Do not dig or attack automatically whenever a move fails: the obstacle may be protected, valuable, a player or mob, or outside the area the user allowed.

For falling gravel or sand, limit the number of attempts or the elapsed time, check every dig result, and stop with the returned reason on failure. Recheck the block before digging again and retry the move only within the allowed area. An unchecked detect/dig loop has no stop policy for a protected block or a continuing stream of falling material.

Moving uses one fuel per block; turning does not. `turtle.getFuelLevel()` returns a number or `"unlimited"`; the maximum is `turtle.getFuelLimit()`. `turtle.refuel(0)` tests whether the selected item is fuel without using it; pass an explicit count when refueling. Plan fuel for the return trip. Turtles have 16 slots and two upgrade sides; check the actual upgrades and limits instead of copying creative-mode assumptions.

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

GPS gives position but not facing. Track dimension, coordinates, and facing explicitly, and update them only after a confirmed move or turn. If the computer stops after a move but before saving, the saved position is uncertain: re-establish it from GPS or another trusted reference, or stop. A saved step counter does not make navigation exactly-once.

Give every retry a maximum count or time and a reason. Falling blocks, mobs, unloaded chunks, low fuel, and a blocked way home need different responses. An unbounded dig-forward loop is not a recovery strategy.

## Inventory and tasks

Inspect the relevant slots and their real counts; reserve slots for fuel, seeds, or building materials explicitly. Check for free space before collecting, and check the results of `drop`, `suck`, and transfers before updating totals. The selected slot affects digging, placing, refueling, and crafting.

For mining, define the allowed volume and the return route; the ROM `excavate` and `tunnel` programs may already be enough. For farming, read block states with `turtle.inspect` (crop `age`) and the pack's growth rules. For crafting (crafty turtle), confirm the effective recipe and grid layout. For building, check block identity, orientation, replaceability, and remaining materials. Vanilla examples say nothing about modded recipes or protected servers.

Turtles do not keep chunks loaded by themselves; when the chunk unloads the program stops and restarts from `startup` on reload. A chunk-loading upgrade covers only its configured radius, not a whole factory or return route. AP upgrades add peripheral methods, not new `turtle.*` functions.
