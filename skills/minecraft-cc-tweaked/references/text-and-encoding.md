# Text, glyphs, and UTF-8

[Core](../SKILL.md) · [Create display](mod-create.md) · [AP chat](mod-advanced-peripherals.md)

Separate three questions: what bytes the Lua string contains, how an API converts those bytes, and what glyphs the target can draw. Lua strings are byte sequences; `#text` counts bytes, not Unicode characters or display columns.

Native CC terminals/monitors use their character-cell glyph set, not a general Unicode font. They support more than ASCII, but arbitrary Chinese/emoji text does not render merely because a Lua file is UTF-8. Use supported characters or a deliberately installed, reviewed glyph-rendering solution when the task requires it. Do not claim a particular third-party font library is the only possible solution.

Files, JSON, network payloads, mod chat, and Create display targets have different encoding contracts. Non-ASCII data is not inherently invalid Lua. A mod may accept byte tables, an explicit UTF-8 option, or JSON Unicode escapes. Confirm its version-specific protocol and test end to end; do not apply a native monitor limitation to every mod surface.

| Surface | Reviewed baseline path | Verification |
|---|---|---|
| Native term/monitor | Supported character glyphs or installed rendering library | Real dimensions, font, layout |
| Create 6.0.10 DisplayLink | `writeBytes` with an integer byte table | Target/drive, rows then columns, visible text |
| Reviewed AP chat jar | `sendMessage(text, {player=..., utf8=true})` | Receiver/range/configuration, cooldown, actual appearance |
| AP formatted chat | Valid text-component JSON; Unicode escapes when appropriate | JSON parsing and target rendering |

Use `utf8.offset` or another validated decoder to find character boundaries; this is not a general display-width algorithm. Combining characters and emoji can occupy widths unlike codepoint counts. The Create renderer here is limited to valid BMP text and requires real target confirmation.

For fixtures, record the source byte representation. Java-to-Lua conversion may carry UTF-8 bytes through a Latin-1-compatible transport; visually similar strings are not proof that the bytes survived. Inspect byte arrays or decoded output at the relevant boundary.
