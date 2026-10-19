# Troubleshooting

[Core](../SKILL.md) · [Testing](testing.md)

Start with the exact error, program/file/line, runtime, selected device, and recent change. Reproduce the smallest failing boundary. Do not repeatedly replace the whole program based on a symptom alone.

| Symptom | Check | Correction |
|---|---|---|
| `No such program` | Saved file, shell working directory, launch command | Locate the file and run the correct path |
| Indexing nil | Missing wrapper/module/result | Check presence and failed-call result before indexing |
| `bad argument` on peripheral | Dot versus colon, parameter order/type, actual version | Use the verified contract, not a remembered signature |
| Empty/incomplete inventory count | Sparse list, truncated preview, variant grouping | Use full data with `pairs` and correct identity |
| Frozen dashboard or missed command | Callback/sleep/device yields, consumed timer | Separate input listener and yielding work; own timer IDs |
| `Too long without yielding` | Busy loop or large synchronous calculation | Bound work and yield without consuming required listener events |
| Reported success but no action | Only pcall checked, zero/partial movement, async pending | Interpret business values and observe the actual effect |
| Progress resets after restart | Corrupt state defaulted, stale backup, uncertain world action | Preserve generations and reconcile; stop new feed |
| Backup stops advancing | Existing destination, ignored copy/move errors | Check every backup transition and interruption window |
| Recipe stalls or unexpected output | Current recipe overrides, wrong topology/input, unknown progress | Reconfirm effective profile; quarantine ambiguity |
| Target speed changes, no processing | Wrong controller, clutch, stress, missing heat/material | Read actual state and observe the permitted small test |
| Native monitor shows garbled text | Unsupported glyphs versus byte encoding | Use supported glyphs or a verified rendering path |
| Create display has wrong layout | Rows/columns order, target/drive, update failure | Use the baseline adapter and verify the real display |
| AP chat fails/garbles/reorders | Binary profile, options, event order, cooldown, encoding | Discover current methods and test one adapter call |
| Startup addition never runs | Earlier long-running entry or disk/settings precedence | Integrate with existing startup supervision |
| HTTP fails | Server policy, response status, handles, actual API events | Diagnose that boundary; bound retries and close handles |
| Turtle pose diverges | Unchecked move/turn or crash before saving | Stop and re-establish pose before continuing |

Read-only discovery is preferable to speculative world changes. If a failure can follow a partial physical effect, inspect the affected source/work/destination before retrying. If evidence is incomplete, state what remains unknown rather than guessing a completed action.
