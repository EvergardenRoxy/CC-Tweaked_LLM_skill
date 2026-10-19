# Design from requirements

[Core](../SKILL.md) · [Events](events-and-concurrency.md) · [Recovery](state-and-recovery.md)

## Derive the design

Translate the goal into inputs, decisions, outputs, and evidence of completion. Identify actors that can change the same world state: players, hoppers, other computers, and machines. Record the current installation and authorized actions once; do not repeatedly ask for facts already established.

Choose the smallest suitable structure:

| Workload | Structure | Boundary |
|---|---|---|
| One inspection or edit | Straight-line script | Check each external result |
| Periodic read-only status | Polling loop | Sleeping is acceptable if other events are irrelevant |
| Short non-yielding event callbacks | One event loop with owned timers | A yielding callback can disrupt input handling |
| Commands plus yielding device reads/actions | Listener, bounded queue, workers | Shared state still needs explicit ownership |
| Multi-step physical work | State machine and observation | A timeout is uncertainty, not proof of failure |
| Work surviving reboot | Persisted intent and reconciliation | Disk and world changes are not one transaction |

For every external interaction ask: can it be absent, slow, rejected, partly completed, repeated, or completed before an error? Choose a bounded response and explain how the user sees it.

## Data and ownership

Give one component ownership of each actuator and production ledger. Let observation workers publish snapshots; let command handlers submit requests. Avoid independent workers feeding the same workpiece. If a decision spans a yielding call, revalidate the assumptions afterwards.

Keep current recipe/configuration data outside control flow. Confirm effective ingredients, tags, steps, repetitions, and outputs before processing. A packaged example establishes neither the current recipe nor the physical route. See [recipe-driven production](recipes-and-production.md).

Bound accepted work and retry budgets. Reject new requests explicitly when capacity is exhausted. Old telemetry can be replaced when only the newest value matters; accepted orders, replies, and settlement records cannot be silently evicted.

## Review an existing program

Trace one request through acceptance, persistence, action, verification, delivery, and restart. Check complete API return values at each boundary. Look for hidden resets, swallowed errors, misleading success messages, ambiguous device selection, and assumptions copied from an older environment.

Change one related behavior group at a time. Reproduce the failure, repair the responsible boundary, run a relevant regression case, and verify dependent paths. Do not add a UI, network service, authentication layer, or distributed architecture unless the task needs it.
