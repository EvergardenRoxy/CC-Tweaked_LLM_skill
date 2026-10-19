# Getting started and startup integration

[Core](../SKILL.md) · [API guide](api-reference.md)

The CraftOS prompt runs program names. `edit example.lua` opens the editor; save a Lua file, exit, then run `example`. The `lua` program is a separate interactive Lua interpreter. Pasting a whole program into the shell prompt is not file installation.

Start manually before enabling automatic startup. Keep an existing entry point and application files intact. Choose an application directory, data directory, and launcher compatible with the existing boot arrangement.

In the inspected CC:T 1.120.2 ROM startup implementation, root `startup`/`startup.lua` and files under a `startup` directory can all be selected, then run **sequentially**. A long-running earlier launcher prevents later entries from being reached. Disk startup and settings can change which startup set is selected. Therefore adding a file under `/startup/` is not a universal coexistence solution. Inspect the installed ROM/settings and integrate with the user's current supervisor or entry point.

Keep a manual recovery route: know how to terminate the application, disable its launcher, or use permitted recovery media. Test restart only after saving relevant user state. Ctrl+T termination and Ctrl+R reboot are normally held key combinations in the game client; they do not provide transactional cleanup.

## Reading signatures

`method(required [, optional])` means brackets document an optional argument; they are not typed into Lua. Multiple return values are separate values. A value can be nil, a result table, a reason string, or a returned object; check the specific contract.

Use the game's `help`, installed ROM, and [official documentation](https://tweaked.cc/). An external editor can improve editing but does not automatically synchronize files into the computer. Confirm any transfer tool and destination before replacing files.

For unsupported non-Latin text, distinguish native terminal glyph limitations from UTF-8 file or mod transport; see [text and encoding](text-and-encoding.md). For testing outside Minecraft, see [testing](testing.md).
