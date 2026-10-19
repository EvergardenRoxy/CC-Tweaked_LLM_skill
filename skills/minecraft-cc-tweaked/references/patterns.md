# Small patterns and adaptation boundaries

[Core](../SKILL.md) · [Design](design-thinking.md)

These are building blocks, not complete factories. Pick a pattern from the task's real constraints; do not rename a large template and assume its world fits the user's.

| Goal | Starting point | Adapt before use |
|---|---|---|
| Inventory summary | Full sparse-list aggregation in [peripherals](peripherals.md) | Item variants, reads that are not a snapshot, explicit device choice |
| Status plus commands | Listener/worker/poller in [events](events-and-concurrency.md) | Event sources, queue size, which task drives outputs, shutdown |
| Durable material action | Persistence gate in [recovery](state-and-recovery.md) | A real save function, observed completion, reconciliation on restart |
| Presentation preferences | Normalized config in [engineering](app-engineering.md) | Which fields, how durable; never reuse it for production state |
| Create multiline display | Byte-table renderer in [Create](mod-create.md) | Actual target, BMP-only text, failed updates |
| AP private reply/chat input | Options/event adapters in [AP](mod-advanced-peripherals.md) | Exact AP version, cooldown, who may command, what success means |
| Turtle work | Bounded motion with observed results in [turtles](turtle.md) | Allowed area, position and facing, fuel, materials, interruption |
| Recipe automation | Effective profile in [production](recipes-and-production.md) | Current recipe, machine layout, completion evidence, limits |

## Bounded read-only sampling

```lua
local function sample_energy(store)
    local energy = store.getEnergy()
    local capacity = store.getEnergyCapacity()
    if type(energy) ~= "number" or type(capacity) ~= "number" or capacity <= 0 then
        return nil, "No valid energy capacity"
    end
    return { energy = energy, capacity = capacity,
             fraction = math.max(0, math.min(1, energy / capacity)) }
end
return sample_energy
```

The two reads are not taken at the same instant. This helper is for display. Switching generators automatically also needs the actual signal polarity, on/off thresholds with a gap between them (hysteresis), a policy for device failure, and the user's permission.

This skill deliberately has no templates for password doors, homemade authentication or hashing, factories built on assumed vanilla recipes, unbounded digging loops, or wrappers that claim a checkpoint makes an action exactly-once. Build those from verified contracts when the task needs them.
