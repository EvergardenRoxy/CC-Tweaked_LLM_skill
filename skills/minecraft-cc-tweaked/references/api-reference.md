# Core API guide

[Core](../SKILL.md) · [Official API index](https://tweaked.cc/)

This is a navigation guide, not a copy of every signature. Verify optional APIs and arguments against the installed CC:T version. Device-specific APIs may be absent.

| Domain | Main operations | Contract to remember |
|---|---|---|
| `os` | `pullEvent`, `pullEventRaw`, `queueEvent`, `startTimer`, `cancelTimer`, `clock`, `epoch`, labels/IDs | Timer IDs and event payloads matter; clocks have different purposes |
| `fs` | `open`, `exists`, `isDir`, `list`, `combine`, `copy`, `move`, `delete`, `getFreeSpace` | Paths are filesystem-root-relative, not shell-working-directory-relative; operations can fail |
| File handles | `read`, `readLine`, `readAll`, `write`, `writeLine`, `flush`, `close` where supported | Check open errors and write/close exceptions; always close acquired handles |
| `textutils` | `serialise`, `unserialise`, `serialiseJSON`, `unserialiseJSON` | Decode success still needs schema validation; JSON options are version-sensitive |
| `settings` | `define`, `get`, `set`, `load`, `save` | Define types/ranges and inspect persistence results; not a production transaction log |
| `term` / terminal objects | `getSize`, `setCursorPos`, `write`, `blit`, colors, palette, `redirect` | Size is columns, rows; redirect is shared process state |
| `window` | `create` | Hide while drawing and reveal/redraw to reduce flicker |
| `colors` / `colours` | Color constants, `combine`, `test`, `subtract`, RGB packing | Color values are bit masks; some devices only support grayscale |
| `paintutils` | Images, lines, boxes, pixels | Drawing uses terminal character cells |
| `redstone` / `rs` | Digital/analog/bundled input and output | Match actual wiring and polarity; analog levels differ from booleans |
| `peripheral` | Discovery, types, methods, wrapping, calls, names | A peripheral can have several types; wrappers use dot calls |
| `parallel` | `waitForAny`, `waitForAll` | Cooperative; returning one task can end its siblings with waitForAny |
| `rednet` | `open`, `send`, `broadcast`, `receive`, `host`, `lookup` | No built-in cryptographic authentication or delivery guarantee |
| `http` | Requests, URL checks, WebSockets | Server policy and resource limits apply; close responses/sockets |
| `gps` | `locate` | May fail; position does not establish turtle orientation |
| `shell` | `run`, `resolve`, `resolveProgram`, directories/path | Provided in shell program environments, not every raw `os.run` environment |
| `multishell` | Tabs and focus | Advanced-computer/runtime availability varies |
| `disk` | Media, mount paths, labels, audio | Takes drive names, not arbitrary file paths |
| `pocket` | Upgrade management | Pocket devices only |
| `commands` | Minecraft command execution | Command computers and server permissions only |

Use `require` for supported `cc.*` modules, such as `cc.expect`, `cc.pretty`, `cc.completion`, `cc.audio.dfpwm`, and `cc.strings`. Probe optional modules rather than inventing fallback globals. Use the installed documentation for version-specific additions.

## Lua conventions

Use `local`, `~=` for inequality, `..` for concatenation, and `table.pack`/`table.unpack` with `.n` when nil-bearing return tuples matter. Wrapped CC APIs do not receive an implicit `self`.

Do not assume host facilities such as `os.execute`, `os.getenv`, `io.popen`, `collectgarbage`, or Lua 5.3 integer operators exist. Test code on the target runtime; a host Lua compiler is a syntax check only. Avoid a single enormous function with hundreds of locals; use modules.

JSON/Lua deserialization is for data. Do not replace it with `load` on untrusted configuration or network messages. Empty environments alone do not make arbitrary code safe to execute.
