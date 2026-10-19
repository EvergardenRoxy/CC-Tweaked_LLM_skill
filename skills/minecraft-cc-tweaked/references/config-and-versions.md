# Configuration, versions, and sources

[Core](../SKILL.md) · [Official documentation](https://tweaked.cc/) · [CC:T repository](https://github.com/cc-tweaked/CC-Tweaked)

Record Minecraft, loader, CC:T, relevant mods, device kind, and configuration when they affect the task. Read `_HOST` or exposed APIs where useful; do not infer the entire server from one version string. A matching filename/version is weaker evidence than a verified binary and current behavior.

## Configuration to inspect when relevant

| Area | Environment-dependent behavior |
|---|---|
| HTTP/WebSocket | Enablement, allowed hosts/ports, private-network rules, redirects, limits |
| Filesystem | Disk quota, free space, read-only mounts, available handle modes |
| Runtime | Execution budget, event capacity, timing under lag |
| Turtles | Fuel mode/limits, permissions, upgrades, movement/chunk loading |
| Startup | Startup settings, disk precedence, sequential existing launchers |
| Mods | Enabled peripherals, owner/permission rules, cooldowns, ranges, energy costs |
| Recipes | Datapack/script overrides, tag resolution, conditions, outputs, loop/chance model |

Do not supply remembered default limits as universal requirements. A simulator's disk/fuel/timing policy is not proof of the live server's policy. Prefer read-only queries and supplied configuration over changing settings just to make a test pass.

## Compatibility strategy

Use official installed documentation/release notes for the target version, and capability probes for optional methods or modules. Generic handler availability, multi-type peripherals, audio, redstone relays, data components, and newer libraries vary across releases. Do not call a feature solely because a current online API page lists it.

Host Lua 5.2 compilation catches many syntax errors, but Cobalt and CraftOS globals/library behavior still need target-runtime checks. Keep unsupported host facilities out of production code.

Legacy ComputerCraft tutorials, translations, decompiled classes, and generated indexes are supporting references. Resolve conflicts against the actual target: core API implementation for core behavior, current mod implementation for adapter contracts, and effective server data/configuration for production rules. For reviewed Create/AP artifacts, read [the baseline](mod-source-baseline.md).
