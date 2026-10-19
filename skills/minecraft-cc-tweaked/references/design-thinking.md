# Design from requirements

[Core](../SKILL.md) · [Events](events-and-concurrency.md) · [Recovery](state-and-recovery.md)

## Derive the design

1. Restate the goal as a result, then translate it into CC primitives: inputs (events, polled peripherals, redstone, network, timers), decisions, outputs, state that must persist, and the evidence that shows the work is done.
2. List who else changes the same world state: players, hoppers, other computers, machines.
3. List the constraints below that apply.
4. Choose the smallest structure that fits, and say why.
5. Analyze failure for every external interaction.
6. Plan observability and how the user will verify it step by step.

Record the installation and authorized actions once; do not ask again for facts already given.

## Hard constraints of the CC world

| Constraint | Design consequence |
|---|---|
| Time resolution is one game tick (0.05 s); `sleep` and timers round up | No logic that needs finer timing |
| Server lag makes ticks slower than real time | Use `os.epoch("utc")` for anything tied to real time (audio, web services), not tick counts |
| Peripheral methods usually wait a tick, and events arriving meanwhile are lost to that coroutine | Batch or cache calls; keep event waiting and device calls in different coroutines |
| No yield for too long stops the program | Yield periodically in heavy computation |
| Filtered waits discard other events; the queue holds about 256 | Keep few waiting points; throttle high-rate event sources |
| Chunk unload = shutdown, memory cleared | Persist progress and resume from `startup` with reconciliation |
| Peripherals can be removed or renamed at any time | Configurable names, protected calls, `peripheral`/`peripheral_detach` handling |
| Networks lose, delay, and time out; HTTP can be disabled | Timeouts, bounded retries, fallbacks |
| Rednet can be overheard and forged | Mention the risk for doors, valuables, or remote control; add authentication only when needed ([security](security.md)) |
| Disk around 1 MB by default, limited memory | Do not cache large data |
| Native screens draw 256 glyphs, no Chinese | English UI text by default ([text and encoding](text-and-encoding.md)) |
| Anyone with physical access can break the machine or read its files | No secrets stored on the computer |

## Choose the structure

| Workload | Structure | Boundary |
|---|---|---|
| One task, then exit (dig one tunnel, sort a chest once) | Straight-line script | Check each result; print the reason and exit on failure |
| Periodic read-only status | `while true do work() sleep(N) end` | Fine when no other events matter |
| Several event types plus a timer, handlers make no waiting calls | One event loop with owned timers | A yielding handler breaks it |
| Polling devices plus commands or touch | Listener, bounded queue, worker, poller in `parallel` | Shared state still needs one owner |
| Independent long-running services | `parallel.waitForAny/All`, communicating through shared tables or custom events | Plan shutdown and errors |
| Multi-step physical work with clear phases | State machine plus observation | A timeout means uncertainty, not failure |
| Work that must survive reboot | Persisted intent and reconciliation | Disk and world changes are not one transaction |
| Too much for one computer, or spread out | Several computers with a message protocol | Each computer has one role; messages have type, version, timeout |

## Failure analysis

For every peripheral call, turtle action, network request, and file operation, ask:

1. **It fails** (false/nil or an error): check results; use `pcall` where needed.
2. **It never returns** (hung request, stuck machine): timeout or watchdog timer.
3. **The target disappears** (peripheral removed, file deleted, HTTP disabled): find it again, degrade, tell the user.
4. **It repeats or arrives out of order** (resent message, late response, double click): request IDs, sequence numbers, idempotent operations.
5. **It succeeds partly, or succeeds and then raises an error**: read the state back before a bounded retry.

Not every answer needs code, but each must be a deliberate decision: some failures may simply stop the program, others must recover automatically.

## Patterns

- **Data-driven rules.** For storage and sorting, describe the work as data (source, destination, filter, amount, priority) and keep the code an interpreter of rules. Validate rules on load; isolate each rule with `pcall` so one bad rule is reported without stopping the rest.
- **Containers that are both source and destination.** Prevent items bouncing back and forth: make input and output filters exclusive, split the buffer into an input chest and an output chest, or track what the system itself delivered.
- **Persisted state and startup reconciliation.** Save the intent before changing the world and the confirmed result after. On startup, compare the record with the real world (inventories, redstone, position); the world wins and the file is a clue. See [state and recovery](state-and-recovery.md).
- **Startup self-check and observability.** Check required peripherals and types at startup and fail immediately with a clear message ("front needs an inventory, found nil"). Keep counters (handled, failed, rejected, queue depth) visible on screen or in a log line, so the user can report numbers.
- **Message protocols.** Messages are tables `{ type = ..., version = 1, id = ... }`; ignore unknown types; replies carry the request ID; clients time out. Ignore echoes of your own broadcasts. Keep periodic status and commands on separate protocols. Keep a simple fallback controller for critical actions such as an emergency stop.
- **Custom events between programs.** `os.queueEvent("myapp_command", instance, ...)` lets a UI control a background service on the same computer; events cannot carry functions. Replaying input events received over rednet lets anyone in range type for you; decide on sender checks with the user.
- **Command-line arguments.** Parse `local args = { ... }`; on missing or invalid arguments print usage and `return`; range-check numbers from `tonumber`.
- **Capability detection and fallback.** Check optional APIs with `type(x) == "function"` or `pcall(require, name)`, use the better path when present, and tell the user what is missing otherwise.

## Data and ownership

Give one component ownership of each actuator and production ledger. Observation workers publish snapshots; command handlers submit requests. Do not let independent workers feed the same workpiece. If a decision spans a yielding call, recheck its assumptions afterwards.

Keep recipe and configuration data out of control flow. Confirm effective ingredients, tags, steps, repetitions, and outputs before processing; a bundled example establishes neither the current recipe nor the physical route ([recipe-driven production](recipes-and-production.md)).

Bound accepted work and retries, and reject new requests visibly when full. Old telemetry may be replaced when only the newest value matters; accepted orders, replies, and settlement records must never be silently dropped.

## Review an existing program or tutorial

1. **Does every function exist?** Check against [the API reference](api-reference.md) and tweaked.cc. Commonly invented: `textutils.sha256`, `os.exit`, `turtle.getPosition`, `peripheral.getAll`.
2. **Are calls right?** `.` versus `:`, argument order, number of return values (`turtle.getItemDetail` returns one).
3. **Are environment assumptions right?** Programs started by `os.run` have no `shell`; `require` path rules; server limits.
4. **Can it lose events or run too long without yielding?**
5. **Are failure paths handled?** Use the five questions above.
6. **Do safety claims hold?** Test any "secure" scheme against [security](security.md).
7. **Is the translation trustworthy?** Machine-translated API descriptions can be badly wrong; trust the full documentation and actual behavior.

Trace one request through acceptance, persistence, action, verification, delivery, and restart. Look for hidden resets, swallowed errors, misleading success messages, and ambiguous device selection. Change one related behavior at a time: reproduce the failure, fix the responsible part, run a regression case. Do not add a UI, network service, authentication, or distributed design unless the task needs it.
