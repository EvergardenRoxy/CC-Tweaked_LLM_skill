# Text, glyphs, and UTF-8

[Core](../SKILL.md) · [Create display](mod-create.md) · [AP chat](mod-advanced-peripherals.md)

Keep three questions apart: which bytes the Lua string holds, how an API converts those bytes, and which glyphs the target can draw.

## Where Chinese and other non-Latin text can go

| Destination | Works? | How | Provider |
|---|---|---|---|
| Native terminal and monitor (`print`, `mon.write`) | **No** | Use English or pinyin and explain why; a community glyph library is possible with prerequisites (below) | CC:T |
| `error`, `printError`, crash messages, `read()` input | **No** | English only | CC:T |
| File contents | Yes, as UTF-8 bytes | Write directly; `#s` counts bytes | CC:T |
| AP chat box, outgoing | Yes, in the reviewed jar | `sendMessage(text, { utf8 = true, ... })`, or formatted JSON with `\uXXXX` escapes | Advanced Peripherals |
| AP chat box, incoming | Yes | Read the `messageUtf8` argument of the `chat` event | Advanced Peripherals |
| Create Display Link to a display board | Yes, in the reviewed jar | `writeBytes(byteTable)`; `write("...")` with UTF-8 garbles | Create |

For any other mod peripheral, try one short message in the game and have the player confirm it looks right before building on it.

## Why: Lua strings are bytes

- A Lua string is a byte sequence. A Chinese character saved in a UTF-8 source file is three bytes, so `#text` counts bytes, not characters or screen columns. `utf8.len` and `utf8.offset` find character boundaries; they do not measure display width (emoji and combining characters break that assumption).
- Native terminals and monitors draw a fixed 256-glyph set (ASCII, drawing characters at 128–159, Latin-1 at 160–255), one glyph per byte. A UTF-8 Chinese character therefore shows as two or three unrelated glyphs.
- **Text from a mod (Java) into Lua** arrives with characters above U+00FF replaced by `?`. Use a separate UTF-8 field when the mod provides one, such as `messageUtf8`.
- **Text from Lua into a mod** usually becomes one Java character per byte, so UTF-8 appears as mojibake such as `å·²`. A mod can only show it correctly through a channel that decodes UTF-8: AP's `utf8` option or JSON escapes, Create's byte table.
- A cct-run trace may show UTF-8 bytes as Latin-1-looking text such as `å·²`. That appearance alone does not prove the game output is garbled: AP's `utf8=true` path intentionally decodes those bytes. Check the byte values and the receiving API's decoding contract, then verify the visible result in the game. A plain Java-string path without UTF-8 decoding will still garble those bytes.

| Surface | Reviewed path | Verify in game |
|---|---|---|
| Native term/monitor | Supported glyphs, or an installed glyph library | Real size, font, layout |
| Create 6.0.10 Display Link | `writeBytes` with an integer byte table | Target and drive, rows then columns, visible text |
| AP 1.21.1-0.8.2a chat | `sendMessage(text, {player=..., utf8=true})` | Receiver, range, configuration, cooldown, appearance |
| AP formatted chat | Valid text-component JSON; Unicode escapes where useful | JSON parsing and appearance |

The Create renderer in [Create](mod-create.md) assumes valid BMP text, one character per column, and still needs confirmation on the real display.

## Chinese on native screens: glyph libraries

When the user explicitly wants Chinese on a CC terminal or monitor, a community library can draw characters from small pixel glyphs with `term.blit`, for example [utf8display](https://git.liulikeji.cn/xingluo/ComputerCraft-Utf8/src/branch/main/utf8display). Explain its prerequisites and get the user's agreement first:

- Font files are large (the 8 px simplified font is about 1.7 MB), more than a default 1 MB computer disk. Without a larger `computer_space_limit`, the font must be downloaded over HTTP at each boot, so HTTP must be enabled and the host allowed.
- Each character takes several cells (with the 8 px font, 4 columns by 3 rows), so only a few characters fit per line; use `setTextScale(0.5)` on monitors.
- It draws to the current `term`; redirect to the monitor first and restore afterwards.
- Only text passed to the library shows Chinese. Errors, crash messages, and `read()` still use native glyphs.
- Wrap library calls in `pcall` and fall back to English if the font fails to load.
- Install a pinned copy with `wget`; do not `load` the remote file on every run (see [security](security.md)). The repository has no license file, so link to it instead of copying its code.

For a status display in a factory, a Create display board is often simpler: no font download and no disk space used.

## Testing text

Record the source bytes in fixtures. To inject Chinese input (for example `messageUtf8`) into cct-run, write each UTF-8 byte as a character no higher than U+00FF, the way the game passes it; raw Chinese in a fixture reaches the program as `?`. Do not add an English command set just to make testing easier: the real Chinese path would stay untested. Visually similar strings do not prove the bytes survived; inspect byte arrays at the relevant boundary, and confirm final appearance in the game.
