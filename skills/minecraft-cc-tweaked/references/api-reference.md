# Core API guide

[Core](../SKILL.md) · [Official API index](https://tweaked.cc/)

This is a navigation guide, not a copy of every signature. Verify optional APIs and arguments against the installed CC:T version. Device-specific APIs may be absent.

| Domain | Main operations | Contract to remember |
|---|---|---|
| `os` | `pullEvent`, `pullEventRaw`, `queueEvent`, `startTimer`, `cancelTimer`, `clock`, `epoch`, labels/IDs | Timer IDs and event payloads matter; clocks have different purposes |
| `fs` | `open`, `exists`, `isDir`, `list`, `combine`, `copy`, `move`, `delete`, `getFreeSpace` | Paths are always from the root, not the shell's current directory (use `shell.resolve` for user input); operations can fail |
| File handles | `read`, `readLine`, `readAll`, `write`, `writeLine`, `flush`, `close` where supported | `fs.open` returns `nil, reason` on failure; its handles use dots (`h.readAll()`), `io` handles use colons (`f:read()`); always close handles |
| `textutils` | `serialise`, `unserialise`, `serialiseJSON`, `unserialiseJSON` | A successful decode still needs its fields validated; JSON options vary by version |
| `settings` | `define`, `get`, `set`, `load`, `save` | `define` declares type and default; check `save` results; not a production ledger |
| `term` / terminal objects | `getSize`, `setCursorPos`, `write`, `blit`, colors, palette, `redirect` | `getSize` returns columns, rows; `term.redirect` affects every later `print` until restored |
| `window` | `create` | Hide a window while drawing, then show it, to avoid flicker |
| `colors` / `colours` | Color constants, `combine`, `test`, `subtract`, RGB packing | Colors are bit masks (combine for bundled cables); basic computers and monitors show grayscale |
| `paintutils` | Images, lines, boxes, pixels | Drawing uses terminal character cells |
| `redstone` / `rs` | Digital/analog/bundled input and output | Match actual wiring and polarity; analog levels differ from booleans |
| `peripheral` | Discovery, types, methods, wrapping, calls, names | A peripheral can have several types; wrappers use dot calls |
| `parallel` | `waitForAny`, `waitForAll` | Cooperative; `waitForAny` stops the others when one returns |
| `rednet` | `open`, `send`, `broadcast`, `receive`, `host`, `lookup` | No built-in cryptographic authentication or delivery guarantee |
| `http` | Requests, URL checks, WebSockets | Server policy and resource limits apply; close responses/sockets |
| `gps` | `locate` | May fail; position does not establish turtle orientation |
| `shell` | `run`, `resolve`, `resolveProgram`, directories/path | Available to programs started from the shell, not in every `os.run` environment |
| `multishell` | Tabs and focus | Advanced computers only |
| `disk` | Media, mount paths, labels, audio | Takes a drive's side or network name, not a file path |
| `pocket` | Upgrade management | Pocket devices only |
| `commands` | Minecraft command execution | Command computers and server permissions only |

Load `cc.*` libraries with `require`, for example `cc.expect`, `cc.pretty`, `cc.completion`, `cc.audio.dfpwm`, `cc.strings`, and `cc.image.nft`. `require` searches relative to the running program's directory; use `require("lib.util")` for subdirectories. Check that an optional module exists (`pcall(require, name)`) instead of inventing fallback globals.

## Lua conventions

Use `local`, `~=` for inequality, `..` for concatenation, and `table.pack`/`table.unpack(t, 1, t.n)` when return values may contain nil. CC APIs and wrapped peripherals take no implicit `self`, so call them with `.`. Program arguments are `...` (`local a, b = ...`); there is no `arg` table.

`os.execute`, `os.exit`, `os.getenv`, `io.popen`, `collectgarbage`, and Lua 5.3 operators do not exist; delete files with `fs.delete` and exit with `return` or `error("message", 0)`. A host Lua compiler only checks syntax. A function with more than 200 locals fails to compile; split large programs into modules.

Use `textutils.unserialise`/`unserialiseJSON` for data. Never `load` untrusted configuration or network messages; an empty environment does not make arbitrary code safe.
