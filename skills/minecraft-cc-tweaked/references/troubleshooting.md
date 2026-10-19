# Troubleshooting

[Core](../SKILL.md) · [Testing](testing.md)

Start from the exact error text, file and line, CC:T version, the device involved, and what changed recently. Reproduce the smallest failing part. Do not rewrite the whole program based on a symptom alone.

| Symptom | Check | Correction |
|---|---|---|
| `No such program` | Lua typed at the shell, file not saved, wrong directory | Run `lua` for single calls; check with `ls`; run the correct path |
| `attempt to index ? (a nil value)` | `wrap`/`find` returned nil, missing module, failed call result | Check for nil before indexing; print `peripheral.getNames()` |
| `attempt to call nil` | Misspelled or wrong-case name, API missing on this device, method not on this peripheral | Check `peripheral.getMethods(name)` and the docs |
| `bad argument` on a peripheral call | `:` instead of `.`, wrong argument order/type, different version | Use `.` and the verified signature |
| Inventory count too low or empty | `ipairs` on a sparse list, truncated preview, variants merged | Use `pairs` over the full list; group by the right identity |
| Frozen dashboard or missed command | `sleep` or a peripheral call swallowed the event or timer | Separate the input listener from yielding work; compare timer IDs |
| `Too long without yielding` | Busy loop or a long calculation | Wait on an event or `sleep` in the loop; split long work and yield in a worker |
| Reports success but nothing happened | Only the `pcall` flag checked, zero or partial transfer, async job still pending | Check the returned values and observe the actual effect |
| Progress resets after restart | Corrupt state replaced by defaults, stale backup, unknown world state | Keep earlier saves, reconcile with the world, stop new feed |
| Backup stops updating | `fs.copy`/`fs.move` fail when the destination exists, errors ignored | Check every copy/move step and what happens if interrupted |
| Recipe stalls or gives unexpected output | Pack overrides the recipe, wrong layout or input, unknown progress | Re-check the effective recipe; set unknown output aside |
| Target speed changes but nothing processes | Wrong controller, clutch engaged, overstressed, missing heat or material | Read actual speed/stress and run one small permitted test |
| Garbled text on a monitor | Chinese or other UTF-8 text on a native screen | Use English, or a path from [text and encoding](text-and-encoding.md) |
| Create display has the wrong layout | `getSize` returns rows then columns, wrong target, failed update | Use the adapter in [Create](mod-create.md) and check the real board |
| AP chat fails, garbles, or mixes up arguments | Different AP version, options table, event layout, cooldown, encoding | Check `getMethods` and test one call |
| Added startup file never runs | An earlier startup program never exits, or a disk startup takes over | Integrate with the existing launcher |
| HTTP fails | HTTP disabled, host blocked (local addresses by default), error status | Check `http.checkURL`, the status code, and server config; close handles |
| Turtle loses its position | Unchecked move/turn, or stopped before saving | Stop and re-establish position and facing before continuing |
| Program stops when the player leaves | Chunk unloaded | Chunk-load the area; resume from saved state at startup |

Prefer read-only checks over trial world changes. If a failure may have happened after a partial effect, inspect the source, machine, and destination before retrying. If evidence is incomplete, say what is still unknown instead of assuming the action completed.
