---
name: minecraft-cc-tweaked
description: Design, write, review, and debug CC:Tweaked (ComputerCraft, CC:T, CraftOS) Lua programs for Minecraft computers, turtles, pocket and command computers, and their peripherals (monitors, modems, inventories/tanks/energy, speakers, printers, drives, redstone relays), including rednet/GPS, redstone control, HTTP/WebSocket, monitor UIs, and mod peripherals such as Create and Advanced Peripherals. Use when the user mentions CC:Tweaked, ComputerCraft, CC:T, CraftOS, turtles, rednet, peripheral.wrap/find, startup.lua, monitors, wired modems, pastebin/wget, or asks to automate mining, farming, storage, monitoring, factory control, or remote control with Lua in Minecraft.
---

# CC: Tweaked programming

CC:T's Lua environment differs from desktop Lua: a Lua 5.2 runtime (Cobalt), event-driven execution, peripherals addressed by side or network name, and turtle fuel. Many tutorials still show 1.7.10-era ComputerCraft code. **Remembered CC APIs may be wrong or outdated: check them against this skill and [tweaked.cc](https://tweaked.cc/).**

This file holds the rules, workflow, execution model, and quick reference. Read the topic pages in [the reference map](#reference-map) when a task needs their detail; reference examples describe particular environments and never override the user's modpack, server configuration, or instructions.

Use the user's language for explanations and setup instructions. The English-only guidance below applies to text drawn with native terminal/monitor glyphs; it does not require English replies or prohibit verified UTF-8 mod channels.

## Workflow

1. **Restate the goal** as the result the user wants, not the mechanism they mentioned. Break it down: inputs, decisions, outputs, frequency, and what happens on failure.
2. **Prefer the simplest adequate solution**: vanilla redstone/hoppers or an installed mod feature, then ROM programs (`excavate`, `tunnel`, `go`, `refuel`), then a short script, and only then a multi-file application. Offer unrequested features (UI, logging, config files, retry frameworks, authentication) as optional extras.
3. **Ask only what changes the design**, in one message with stated default assumptions. Reuse information already supplied. When the request is explicit and complete, implement it directly and state your assumptions; do not add a confirmation round.
4. **Establish the environment**: CC:T version (`print(_HOST)`), Minecraft version and loader, device kind, peripheral sides or network names, mod versions, server limits, and existing `startup` files. Discover methods with `peripheral.getMethods`; never invent an API.
5. **Design from constraints** (see [design](references/design-thinking.md)): yielding calls, lost events, chunk unloading, disconnecting peripherals, unreliable networks, disk space, and who else changes the same inventories. For each external call ask: can it be absent, fail, partly succeed, repeat, or succeed and then raise an error?
6. **Validate and deliver.** Check the code against the [delivery checklist](#delivery-checklist), test with available tools, and report what ran and what still needs the game.

## Rules

1. **Lua 5.2 syntax only.** No `//`, `&`, `|`, `~` (bitwise), `<<`, `>>`, integer subtype, or `math.type`. Use `math.floor(a / b)` and `bit32.*`. `goto`, `table.pack`/`table.unpack`, `utf8`, and `load(src, name, "t", env)` are available. `collectgarbage`, `os.execute`, `os.exit`, `os.getenv`, `os.remove`, and `io.popen` do not exist.
2. **CC APIs and wrapped peripherals use `.`**: `turtle.forward()`, `peripheral.wrap("top")`, `chest.list()`, `mon.write("x")`. Colon calls are for Lua objects that take `self`: `io` file handles (`f:read("l")`), `vector` objects, string methods (`s:sub(1, 3)`), and your own objects. `fs.open` handles use dots: `h.readAll()`, `h.close()`.
3. **Use real peripheral names.** Adjacent devices use a side: `top`, `bottom`, `left`, `right`, `front`, `back`. Devices on a wired network use the name printed when the modem is activated, such as `minecraft:chest_0`. Check `wrap`/`find` results for `nil` and fail with `error("message", 0)`. When several devices match, select and store an explicit name instead of taking the first `find` result.
4. **Check results; most failures do not raise errors.** Turtle actions return `false, reason`; `fs.open`, `http.get`, `peripheral.wrap`, and `rednet.receive(protocol, timeout)` can return `nil`. `pcall` only reports whether an error was raised: a returned `false`, `nil`, or zero items moved is still a failure. Keep the complete return tuple.
5. **Every long-running loop must yield**, or the computer stops it with `Too long without yielding`. Use `os.pullEvent`, `sleep`, or an operation verified to yield on the target runtime. Native terminal/monitor drawing and some other peripheral methods return immediately; calling them in a loop does not make that loop yield.
6. **Waiting discards other events.** `sleep`, filtered `os.pullEvent`, `rednet.receive`, and peripheral methods that wait for the server all drop the unrelated events that arrive meanwhile. Generic inventory/tank/energy methods and most mod methods wait at least one game tick. To poll devices *and* respond to touches/keys/chat, run a non-yielding listener and the device work in separate `parallel` tasks ([events](references/events-and-concurrency.md)).
7. **`inventory.list()` and `fluid_storage.tanks()` are sparse**: iterate with `pairs`. `pushItems`/`pullItems` take the other peripheral's **name string** (`peripheral.getName(other)`), and both containers must be on the same wired network. Transfers return the count actually moved.
8. **Turtle movement uses fuel** (turning does not). `turtle.getFuelLevel()` may return `"unlimited"`; test for it before comparing numbers. Handle falling gravel/sand, mobs, full inventories, and fuel for the return trip. Never dig or attack blindly when a move fails.
9. **Unloading a chunk stops the computer** and loses all variables; it boots again from `startup` when reloaded. Save progress that must survive to a file, and reconcile it with the world on restart: a saved intent is not proof the action happened.
10. **Preserve existing startup files.** CraftOS runs root `startup`/`startup.lua` and every file in `/startup/` **one after another**; a long-running earlier program blocks later ones, and an enabled disk startup replaces the computer's own set. Integrate with the user's existing launcher instead of overwriting it or assuming `/startup/` runs concurrently ([getting started](references/getting-started.md)).
11. **Native terminals and monitors cannot show Chinese or other non-Latin text**: they draw a fixed 256-character set, so UTF-8 text appears as garbage. Use English UI strings and explain why; comments may use any language. For mod chat or displays, follow [text and encoding](references/text-and-encoding.md).
12. **Never run received data as code.** Do not `load` network, chat, or HTTP text. Rednet protocols, channels, computer IDs, and hidden chat are not authentication. Add authentication only when the user needs it, after defining the threat ([security](references/security.md)).
13. **Mod peripherals are not CC:T.** Their types and methods change between mod versions. The `mod-*` pages describe specific reviewed jars; confirm with `peripheral.getMethods` in the user's game.
14. **Production depends on the current recipes.** Modpacks change recipes, tags, loop counts, outputs, and chances. Confirm the effective recipe before using it as a control condition, and count delivered products, not expected yield ([production](references/recipes-and-production.md)).
15. **Do not claim tests you did not run.** Separate static checks, simulator runs, injected events, and real game observations ([testing](references/testing.md)).

## Execution model

```text
Each computer runs one Lua program in a coroutine, driven by events:
  os.pullEvent(filter)  yields until a matching event arrives; others are discarded
  sleep(n)              = os.startTimer(n) + wait for that timer only
  main-thread methods  yield while waiting for the server; unrelated events delivered
                       to that coroutine meanwhile are discarded
  immediate methods    return without yielding (including native terminal/monitor drawing)
  event queue           holds about 256 events; overflow is dropped
  no yield for seconds  "Too long without yielding"; the program is stopped
```

`parallel.waitForAny/waitForAll` switch between coroutines when one yields; nothing runs truly in parallel. Timers and main-thread work use game ticks (nominally 0.05 seconds); server lag can make them take longer in real time. Do not assume every peripheral method yields or that a main-thread call finishes within one tick.

| Need | Structure |
|---|---|
| Do something every N seconds, no input | `while true do work() sleep(N) end` |
| React to one event type | `while true do local e, a, b = os.pullEvent("monitor_touch") ... end` |
| Timer plus input, no waiting calls in handlers | One `os.startTimer` loop that checks timer IDs (below) |
| Poll peripherals plus react to touch/keys/chat | `parallel`: listener queues commands, worker acts, poller reads devices ([events](references/events-and-concurrency.md)) |
| Many independent peripheral reads | Wrap them as functions and run with `parallel.waitForAll` |
| Progress that must survive reboot | Persisted intent plus reconciliation ([state and recovery](references/state-and-recovery.md)) |

```lua
local INTERVAL = 5
local timer = os.startTimer(INTERVAL)
while true do
    local event, p1 = os.pullEvent()
    if event == "timer" and p1 == timer then
        print("tick", os.clock())
        timer = os.startTimer(INTERVAL)
    elseif event == "key" and p1 == keys.q then
        print("bye")
        break
    end
end
```

## Quick reference

```lua
local mon = peripheral.find("monitor") or error("No monitor attached", 0)
local chest = peripheral.wrap("minecraft:chest_0")
if not chest then error("minecraft:chest_0 not found; is its wired modem enabled?", 0) end
for _, name in ipairs(peripheral.getNames()) do print(name, peripheral.getType(name)) end
```

| Topic | Usage |
|---|---|
| Discovery | `peripheral.getNames()`, `isPresent(name)`, `getType(name)` (may return several types), `hasType(name, type)`, `getMethods(name)`, `getName(wrapped)` |
| Wired network | Attach a wired modem to the computer and to each device, connect them with cable, right-click each device's modem to connect it (it shows the network name in chat). Changes fire `peripheral` / `peripheral_detach` |
| Inventories | `for slot, item in pairs(inv.list()) do ... end`; `inv.pushItems(peripheral.getName(dest), slot [, limit [, toSlot]])`; `size()`, `getItemDetail(slot)` |
| Fluids / energy | `tanks()` (sparse, mB), `pushFluid(toName [, limit [, fluidName]])`; `getEnergy()`, `getEnergyCapacity()` (FE) |
| Turtles | Check `ok, reason` from `turtle.forward()` and `turtle.dig()`; bound retries for falling blocks and stop on failure ([turtles](references/turtle.md)); `turtle.refuel(0)` tests whether the selected item is fuel |
| Redstone | `redstone.setOutput("back", true)`, `setAnalogOutput("top", 7)`, `getInput("left")`; wait with `os.pullEvent("redstone")`; remote sides via `redstone_relay` (1.114.0+) |
| Rednet | `peripheral.find("modem", rednet.open)`; `rednet.send(id, tbl, "proto")`; `rednet.receive("proto", timeout)`; no encryption or delivery guarantee |
| Monitors | `mon.setTextScale(0.5)` (0.5 to 5); `mon.setCursorPos(1, 1)`, `mon.write("x")` (no wrapping); `getSize()` returns columns, rows; touch (`monitor_touch`, name, x, y) on advanced monitors only |
| Files | `fs` paths are absolute from the root; `fs.combine(a, b)`; tables via `textutils.serialise`/`unserialise` or `serialiseJSON`/`unserialiseJSON` |
| Startup | `/rom/autorun`, then disk startup if `shell.allow_disk_startup` is set, otherwise root `startup`/`startup.lua` and `/startup/*` in sequence; `os.setComputerLabel("name")` names the computer |

Version-sensitive features (check `_HOST` before relying on them):

| Feature | Since CC:T |
|---|---|
| Generic `inventory`, `fluid_storage`, `energy_storage` peripherals | 1.94.0 |
| Multiple peripheral types, `peripheral.hasType` | 1.99 |
| `speaker.playAudio`, `cc.audio.dfpwm` | 1.100 |
| Lua 5.2 features, `fs.open` modes `r+`/`w+` | 1.109.0 |
| `redstone_relay` | 1.114.0 |
| `turtle.getEquippedLeft`/`getEquippedRight` | 1.116.0 |
| `commands.getDimension` | 1.119.0 |
| `spawn` argument to `parallel.waitForAll` functions | 1.120.0 |
| `turtle_storage` | 1.121.0 |

## Common mistakes

| Wrong | Result | Right |
|---|---|---|
| `turtle:forward()`, `mon:write("x")` | `bad argument` error | `turtle.forward()`, `mon.write("x")` |
| `peripheral.wrap("chest")` | `nil`, then `attempt to index` | A real side/network name, or `peripheral.find("inventory")` |
| `ipairs(chest.list())` | Stops at the first empty slot | `pairs(chest.list())` |
| `chest.pushItems(otherWrapped, slot)` | Error | `chest.pushItems(peripheral.getName(otherWrapped), slot)` |
| Busy `while true do if rs.getInput("top") then ... end end` | `Too long without yielding` | `os.pullEvent("redstone")` or `sleep` in the loop |
| Waiting for rednet during `sleep(5)` | Message lost | `rednet.receive(proto, timeout)` or `parallel` |
| Chat/touch handling and `chest.list()` in one loop | Missed commands; frozen dashboard after a lost timer | Listener, worker, and poller in `parallel` |
| Unchecked `turtle.forward()` | Position model drifts after a block or empty fuel | `if not turtle.forward() then ... end` |
| `turtle.getFuelLevel() < 100` | Error when fuel is `"unlimited"` | Check `== "unlimited"` first |
| `mon.write(chinese_text)` with UTF-8 Chinese | Garbled glyphs | English text, or a mod path from [text and encoding](references/text-and-encoding.md) |
| `if pcall(chest.pushItems, ...) then` | Zero moved reported as success | Check the returned count |
| Overwriting the user's `startup.lua` | Their existing launcher is lost | Integrate with it; test manually first |
| A crashing or endless `startup.lua` | Breaks every boot | Run it manually first; hold Ctrl+T to stop it; boot from a disk if needed |

More symptoms are in [troubleshooting](references/troubleshooting.md).

## Delivery format

For an unclear request, first reply with: the goal as understood, the breakdown, options from simplest to most complete with their limits, a recommendation, and only the questions that change the design (with defaults). For a program, deliver:

- **Approach**: what the program does and how its loop works; key design decisions and handled failures.
- **Setup**: a table of devices, sides or network names, and purpose.
- **Program**: file path (for example `/stockboard.lua`) and the full code.
- **Install and run**: `edit name`, `wget`/`pastebin get` where HTTP is allowed; how to start, stop (hold Ctrl+T), and reboot (hold Ctrl+R).
- **Verify**: which calls to try in `lua` first and what correct output looks like; if tested, what ran, under which tool, and what was not covered.
- **Risks**: fuel, chunk loading, peripheral names, server config, performance, security.
- **Optional extras**: useful features you deliberately left out.

Scale this to the task; a one-line fix needs one sentence of explanation.

## Reference map

Read only the pages the task needs.

| Task | Reference |
|---|---|
| First program, editor, running files, existing startup | [Getting started](references/getting-started.md) |
| Deriving a design, failure analysis, reviewing code | [Design](references/design-thinking.md) |
| Core APIs and `cc.*` libraries | [API reference](references/api-reference.md) |
| Inventories, fluids, energy, monitors, speakers, printers, drives | [Peripherals](references/peripherals.md) |
| Event loops, timers, `parallel`, work queues | [Events and concurrency](references/events-and-concurrency.md) |
| Saved orders, save failures, interrupted actions, restart | [State and recovery](references/state-and-recovery.md) |
| Effective recipes, sequenced assembly, random outputs | [Recipes and production](references/recipes-and-production.md) |
| Turtle movement, fuel, inventory, navigation | [Turtles](references/turtle.md) |
| Rednet, modems, GPS, HTTP, WebSocket | [Networking](references/networking.md) |
| Terminal/monitor layout and touch | [UI design](references/ui-design.md) |
| Chinese and other non-ASCII text, UTF-8, mod text channels | [Text and encoding](references/text-and-encoding.md) |
| Modules, configuration, logs, installers, updates | [Application engineering](references/app-engineering.md) |
| Passwords, door locks, untrusted remote commands | [Security](references/security.md) |
| Small reusable patterns and their limits | [Patterns](references/patterns.md) |
| Testing with cct-run, fixtures, live game tests | [Testing](references/testing.md) |
| Error messages and symptoms | [Troubleshooting](references/troubleshooting.md) |
| Server configuration, version differences | [Configuration and versions](references/config-and-versions.md) |
| Which mod jars the mod pages describe | [Mod baseline](references/mod-source-baseline.md) |
| Create: speed, stress, displays, Nixie tubes | [Create](references/mod-create.md) |
| Create: packages, stock ticker, trains | [Create logistics](references/mod-create-logistics.md) |
| AP: chat box, player detector, sensors | [Advanced Peripherals](references/mod-advanced-peripherals.md) |
| AP: inventory manager, ME/RS bridges, crafting | [AP storage](references/mod-advanced-peripherals-storage.md) |
| AP: turtle upgrades, smart glasses, optional integrations | [AP extensions](references/mod-advanced-peripherals-extended.md) |
| AP methods on Create blocks (basin, blaze burner, tank) | [Create with AP](references/mod-create-ap.md) |
| Full Create method-name list | [Create method index](references/mod-create-api.md) |
| Full AP method-name list | [AP method index](references/mod-advanced-peripherals-api.md) |

## Delivery checklist

**Syntax and runtime**
- [ ] No Lua 5.3+ syntax or missing functions (rule 1); every variable and function is `local` and defined before use; `~=` for inequality, `..` for concatenation.
- [ ] CC APIs and peripherals are called with `.`; each function exists in this file, [the API reference](references/api-reference.md), tweaked.cc, or the user's `getMethods` output.

**Devices**
- [ ] Peripheral names are real; `wrap`/`find` results are checked for `nil`; the intended device is selected explicitly when several match.
- [ ] `list()`/`tanks()` use `pairs`; transfers pass name strings and check the moved count.
- [ ] Turtles check fuel (including `"unlimited"`), every move/dig result, gravel, and full inventory.
- [ ] Mod methods come from `getMethods` or a `mod-*` page for the stated version, and mod behavior is not presented as CC:T behavior.

**Events and state**
- [ ] Every infinite loop yields; `sleep` is not used where other events matter; timer IDs are compared.
- [ ] Listeners for chat/touch/keys make no waiting peripheral calls; queues are bounded and overload is visible.
- [ ] `os.pullEventRaw` code handles `terminate`.
- [ ] Existing startup files are preserved; progress that must survive is saved, and a failed save stops new material actions.

**Delivery**
- [ ] The simplest adequate solution was chosen; unrequested features are listed as optional.
- [ ] Setup, run steps, verification, version and server-config dependencies, and chunk-loading needs are stated.
- [ ] Native screen text is English; any Chinese output uses a verified path from [text and encoding](references/text-and-encoding.md).
- [ ] Test claims match what actually ran.
- [ ] For long-running programs: bounded network retries with timeouts, `peripheral_detach` handling, recoverable settings, restored palettes/redstone on normal exit, and no secrets in logs.
