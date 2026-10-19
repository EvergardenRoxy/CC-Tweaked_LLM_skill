# Terminal and monitor interfaces

[Core](../SKILL.md) · [Events](events-and-concurrency.md) · [Text](text-and-encoding.md)

Read actual dimensions after selecting the target and scale. Core terminal/monitor `getSize()` returns **columns, rows**. Create DisplayLink in the reviewed artifact returns **rows, columns** and uses a different adapter. Never choose orientation from a copied layout assumption.

Use one layout model for both drawing and hit testing. Match `monitor_touch` to the selected monitor name; native advanced monitors provide touch while basic monitors do not. Handle terminal/monitor resize and clamp all coordinates and progress widths to the current layout.

Show what the user can act on: running/waiting/paused, current task, delivered count, missing input or failed device, and how to stop/resume. Distinguish stale observations and requested targets from measured state. Keep internal implementation details out of ordinary controls.

## Rendering

Use supported native glyphs, aligned columns, and concise labels. Write within bounds; `write` does not wrap automatically. Clear shortened fields or redraw the affected region. Cache a frame only after the adapter's submission succeeds; reconnect, resize, target changes, or external edits should invalidate the cache.

For larger native UIs, draw into a hidden `window` and redraw when complete. Restore redirects/palettes you changed on normal exit where practical. Do not assume cleanup runs after power loss.

For mod displays, verify target, power/drive, encoding, and visible update in the game. An API call without an exception proves only that stage. Codepoint clipping does not guarantee correct emoji/combining-character width.

## Interaction and verification

Keep listeners free of yielding device work. Queue commands with explicit overload behavior and display actionable errors. Destructive/consequential controls should match the task's authorized workflow and physical stop policy.

Test minimum dimensions, long values, zero capacity, missing devices, resize, wrong-source touch, and failed rendering when relevant. A simulated screenshot can establish layout for that fixture; actual readability/fonts and mod target appearance require game observation or user feedback.
