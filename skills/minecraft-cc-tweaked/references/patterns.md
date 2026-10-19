# Small patterns and adaptation boundaries

[Core](../SKILL.md) · [Design](design-thinking.md)

These are building blocks, not complete autonomous factories. Select a pattern from actual constraints rather than copying a large template and assuming its world model applies.

| Goal | Starting point | Adapt before use |
|---|---|---|
| Inventory summary | Full sparse-list aggregation in [peripherals](peripherals.md) | Item variants, sampling consistency, explicit device selection |
| Status plus commands | Listener/worker/poller in [events](events-and-concurrency.md) | Sources, bounded queue, actuator ownership, shutdown |
| Durable material action | Persistence gate in [recovery](state-and-recovery.md) | Real persistence, observed completion, restart reconciliation |
| Presentation preferences | Normalized config in [engineering](app-engineering.md) | Desired fields and durability; never reuse as a production ledger |
| Create multiline display | Byte-table renderer in [Create](mod-create.md) | Actual target, BMP text assumptions, failed updates |
| AP private reply/chat input | Options/event adapters in [AP](mod-advanced-peripherals.md) | Exact binary profile, cooldown, authorization and completion semantics |
| Turtle work | Bounded motion with observed results in [turtles](turtle.md) | Region, pose, fuel, materials and interruption |
| Recipe automation | Effective profile in [production](recipes-and-production.md) | Current recipe, topology, completion evidence and budgets |

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

The two reads need not be an atomic snapshot. This helper is for display data; automatically switching generators requires the actual control polarity, thresholds/hysteresis, device failure policy, and authorization. Do not infer a universal machine controller from an energy fraction.

Old password-door kernels, custom authentication/hash examples, assumed vanilla factory recipes, unbounded digging loops, and "checkpoint means exactly-once" wrappers are intentionally not templates in this skill. Implement the required task from verified contracts instead.
