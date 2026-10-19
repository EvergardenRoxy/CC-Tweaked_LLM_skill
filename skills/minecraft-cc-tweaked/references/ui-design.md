# Terminal and monitor interfaces

[Core](../SKILL.md) · [Events](events-and-concurrency.md) · [Text](text-and-encoding.md)

Read this when the user asks for a dashboard or touch interface. Only the user can judge whether a UI looks good: build a usable version following the rules below, then ask for a screenshot instead of guessing repeatedly.

## Size and purpose first

- Read the real size after choosing the monitor and text scale. Core terminal/monitor `getSize()` returns **columns, rows**; at scale 1 one monitor block holds roughly 7×5 characters, and scale 0.5 doubles that. Do not assume 51×19. Resizing fires `monitor_resize`. Create's Display Link returns **rows, columns** and needs a different adapter ([Create](mod-create.md)).
- Ask who reads it and from how far (large text for distance), whether it needs touch (advanced monitors only), and which information matters most.
- Native monitors have 16 colors (grayscale on basic monitors), one glyph per cell, and no Chinese ([text and encoding](text-and-encoding.md)).

## Layout rules

These rules come from rounds of user feedback on generated dashboards ("bars not aligned", "buttons too small and crowded"):

1. **One set of column positions for every row.** Define the label, value, bar start/width, and number columns once in a table and use it for every row; do not compute positions per row.
2. **Equal-width bars.** Bars in a group share the same start and width. Put numbers (percentages, `12/16384`) in a fixed, right-aligned column to the right of the bars, not wherever a bar ends.
3. **Sidebar for navigation and actions.** Fixed width, a different color from the main panel, entries generated from configuration (a new production line adds a button automatically), and pages when entries exceed the height.
4. **Buttons are full-width color bands with centered text and a blank row between them.** In a two-row button the text looks pushed to the top edge; use three rows with text in the middle for a larger button.
5. **One blank row between groups**, none inside a group, consistently across the screen.
6. **Contrast.** White text on dark or saturated backgrounds (blue, grey, black), black text on light backgrounds; small text on light grey is hard to read. Keep status colors fixed: green normal, yellow attention, red fault, grey unavailable.
7. **Number input with step buttons**: `[-100] [-10] [ amount ] [+10] [+100]` with a display-only middle value, enforced limits, a sensible default (not 1), and a separate confirm button.
8. **Unavailable buttons are grey** with the reason shown nearby or in a status line (for example "owner not nearby"); never a button that silently does nothing.

## Drawing and touch use the same layout

Register each button's area in a table while drawing it, and hit-test `monitor_touch` against that same table. Then layout changes move the touch areas too, and what the user sees always matches what they can press. Match `monitor_touch` to the selected monitor's name, handle resize, and clamp coordinates and bar widths to the current size.

Show what the user can act on: running/waiting/paused, the current task, delivered count, missing input or failed device, and how to stop or resume. Mark stale readings, and keep requested targets visually distinct from measured values. Keep implementation details out of ordinary controls.

## Rendering

- `write` does not wrap and does not clear old text. Write within bounds, and pad or clear a field when its new value is shorter.
- For larger UIs, draw into a hidden `window`, then show it, to avoid flicker. Redraw only on changes or at a modest interval.
- Cache a frame only after drawing succeeded; invalidate the cache on reconnect, resize, target change, or when something else drew on the screen.
- On normal exit, restore any `term.redirect`, palette, and text scale you changed. Cleanup does not run after power loss.
- For mod displays, verify the target, power, encoding, and visible result in the game: a call without an error only proves the call. Cutting text by character count does not handle emoji or combining-character width.

## Interaction and verification

Keep listeners free of waiting peripheral calls. Queue commands with explicit overload behavior and show actionable errors. Destructive controls must match the task's authorized workflow and physical stop policy.

Test the minimum size, long values, zero capacity, missing devices, resize, touches from another monitor, and failed rendering where relevant. A simulator screenshot shows the layout for that fixture; actual readability, fonts, and mod displays need a look in the game or the user's feedback.
