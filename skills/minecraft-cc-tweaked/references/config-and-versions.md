# Configuration, versions, and sources

[Core](../SKILL.md) · [Official documentation](https://tweaked.cc/) · [CC:T repository](https://github.com/cc-tweaked/CC-Tweaked)

Record Minecraft, loader, CC:T, relevant mods, device kind, and configuration when they affect the task. `_HOST` reports the CC:T and Minecraft versions; it does not describe the server's configuration or mods. A matching filename or version label is weaker evidence than the installed binary and its observed behavior.

## Server configuration

The configuration file is `serverconfig/computercraft-server.toml` inside the world folder (single player and servers). Older releases used `config/computercraft-common.toml` or, on Minecraft 1.12.2 and earlier, `config/ComputerCraft.cfg`. Changes take effect after a restart.

The options below are common in recent releases. Names and defaults vary by version and modpack: read the user's actual file rather than assuming these values.

| Option | Typical default | Effect |
|---|---|---|
| `computer_space_limit` | 1000000 bytes | Disk space per computer |
| `floppy_space_limit` | 125000 bytes | Disk space per floppy |
| `maximum_open_files` | 128 | Open files per computer |
| `default_computer_settings` | empty | Default `settings` values for every computer |
| `[http] enabled`, `websocket_enabled` | true | Whether `http` and WebSockets are available |
| `[http] max_requests`, `max_websockets` | 16, 4 | Concurrent requests/sockets |
| `[[http.rules]]` | deny `$private`, then allow `*` | Host rules; `$private` covers local and LAN addresses. Rules can also set size limits and timeouts |
| `[turtle] need_fuel` | true | When false, `turtle.getFuelLevel()` returns `"unlimited"` |
| `[turtle] normal_fuel_limit`, `advanced_fuel_limit` | 20000, 100000 | Maximum fuel |
| `[peripheral] modem_range`, `modem_high_altitude_range` | 64, 384 | Wireless modem range |
| Command-block peripheral option | false | Whether command blocks appear as `command` peripherals |
| `[term_sizes]` | computer 51×19, pocket 26×20 | Terminal sizes |

Reaching a local web server for testing requires removing the `$private` deny rule. Do not suggest that for a public server.

| Area | Other environment-dependent behavior |
|---|---|
| Runtime | Execution time budget, event capacity, timing under lag |
| Turtles | Permissions and protected areas, upgrades, chunk loading |
| Startup | `shell.allow_startup`, `shell.allow_disk_startup`, existing launchers that run in sequence |
| Mods | Enabled peripherals, owner/permission rules, cooldowns, ranges, energy costs |
| Recipes | Datapack/script overrides, tag resolution, conditions, outputs, loop/chance model |

Do not present remembered defaults as requirements. A simulator's disk, fuel, or timing policy is not the live server's policy. Prefer read-only queries and supplied configuration over changing settings to make a test pass.

## `/computercraft` command

| Subcommand | Permission | Effect |
|---|---|---|
| `dump [computer]` | Operator (single player allowed) | List loaded computers: ID, position, running state |
| `turn-on`, `shutdown [computers...]` | Operator | Start or stop computers; with no argument, all loaded computers |
| `tp <computer>`, `view <computer>` | Operator | Teleport to a computer or open its terminal remotely |
| `track start/stop/dump` | Operator | Per-computer execution time and server-task profiling |
| `queue <computer> [args...]` | Everyone | Send a `computer_command` event to a **command computer** |

Computer selectors include `#12` (ID 12) and `@c[id=12]`, `@c[label=name]`, `@c[family=advanced]`, `@c[distance=..100]`.

## Datapack ROM extensions

Datapacks can add files under `data/computercraft/lua/rom/...` (lowercase names): `autorun/` files run at boot, `modules/main/` files can be `require`d, and `programs/` adds programs. Tags such as `computercraft:turtle_can_place` and `computercraft:turtle_can_use` change turtle interaction. The datapack format follows the Minecraft version.

## Version differences

Check the official changelog for exact versions. Notable changes by CC:T version:

| Version | Change |
|---|---|
| 1.80pr1 | Programs run in their own environment; palette API |
| 1.87.0 | `settings.define`; server configuration moved to `serverconfig/` |
| 1.94.0 | Generic `inventory`, `fluid_storage`, `energy_storage` peripherals |
| 1.99 | Multiple peripheral types, `peripheral.hasType` |
| 1.100 | `speaker.playAudio`, `cc.audio.dfpwm` |
| 1.109.0 | **Lua 5.2 runtime**: no `arg` table (use `...`), restricted `getfenv`/`setfenv`, no `string.dump` or binary chunks; files, HTTP, and WebSockets use raw bytes; `fs.open` modes `r+`/`w+` |
| 1.114.0 | `redstone_relay` |
| 1.116.0 | `turtle.getEquippedLeft`/`getEquippedRight` |
| 1.119.0 | `commands.getDimension` |
| 1.120.0 | `parallel.waitForAll` tasks can `spawn` more tasks |
| 1.121.0 | `turtle_storage` |

Minecraft 1.13 changed key codes (always use `keys.*`) and flattened block/item IDs: no metadata in `turtle.inspect` or damage values in item details. Code from 1.7.10/1.12 tutorials that uses `os.loadAPI`, `arg`, numeric key codes, metadata, or methods such as `getStackInSlot` (from addon mods like OpenPeripherals) does not apply to current releases.

## Lua compatibility (Cobalt)

| Available | Not available |
|---|---|
| `goto` and labels, `_ENV`, `\z`, `\xNN`, `\u{XXX}` escapes, `__len`/`__pairs` | Integer subtype, bitwise operators, `//` |
| `bit32`, `utf8`, `string.pack`/`unpack`, `table.move`, `table.pack`/`unpack` | `collectgarbage`, `os.execute`, `os.exit`, `string.dump` |
| `load` with mode and env, `rawlen`, `xpcall` with extra arguments | `math.type`, `math.tointeger`, `math.maxinteger`, `math.ult` |
| `coroutine.isyieldable`, yielding across `pcall` and metamethods | Host facilities such as `os.getenv`, `io.popen` |

Host Lua 5.2 compilation catches many syntax errors, but Cobalt and CraftOS globals still need checks on the target runtime.

## Sources and known discrepancies

Legacy tutorials, translations, decompiled classes, and generated indexes are supporting references. Resolve conflicts against the actual target: the core implementation for core behavior, the installed mod for adapter contracts, and effective server data/configuration for production rules. For the reviewed Create/AP jars, read [the baseline](mod-source-baseline.md).

- `turtle.getItemDetail` returns one value (a table or nil); write `local item = turtle.getItemDetail(slot, true)`.
- `turtle.getFuelLevel()` returns the **current** fuel; the maximum is `turtle.getFuelLimit()`.
- Fuel values, terminal sizes, and configuration defaults come from mod defaults that modpacks can change. Failure reason strings change between versions; ask for the actual output when diagnosing.
- Addon peripherals (Advanced Peripherals, Plethora, and others) are not documented on tweaked.cc; discover them with `peripheral.getMethods`.
