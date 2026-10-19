# Skill contents

[README](README.md) · [Install](INSTALL.md) · [Core entry point](skills/minecraft-cc-tweaked/SKILL.md)

The installed skill is written in English. It consists of one core file and 26 topic references that the agent reads on demand.

## Core: `SKILL.md`

| Section | What it holds |
|---|---|
| Workflow | Restate the goal, prefer the simplest solution, ask only design-changing questions, establish the environment, design from constraints, validate |
| Rules | Lua 5.2 syntax, dot versus colon, peripheral names, checking results, yielding, lost events, sparse inventories, fuel, chunk unloading, startup files, native text limits, untrusted input, mod and recipe boundaries, honest test claims |
| Execution model | How events, `sleep`, peripheral calls, and `parallel` interact; which loop structure fits which need |
| Quick reference | Discovery, wired networks, inventories, fluids/energy, turtles, redstone, rednet, monitors, files, startup, version-sensitive features |
| Common mistakes | Typical wrong code, what happens, and the fix |
| Delivery format | What an answer contains, scaled to the task |
| Reference map | Which topic page to read for which task |
| Delivery checklist | Final checks before handing over code |

## References

| Area | References |
|---|---|
| Foundations | Getting started, API guide, design, configuration and versions |
| Device programs | Peripherals, turtles, UI design, text and encoding |
| Reliability | Events and concurrency, state and recovery, application engineering |
| Production | Effective recipes, topology, observed completion, random-output accounting |
| Communication | Networking and security |
| Delivery | Small patterns, troubleshooting, layered testing |
| Create | Motion/stress/displays, logistics/packages/trains, methods added by AP |
| Advanced Peripherals | Discovery/chat/sensors, storage/crafting, extensions and optional integrations |
| Method lookup | Generated Create/AP method-name indexes with the jars' hashes |

The [reference map](skills/minecraft-cc-tweaked/SKILL.md#reference-map) links every installed page. Exact recipe values found in a reviewed jar are audit findings, not production rules for every pack.

## Outside the installed skill

Development records live under [mod evidence](docs/mod-evidence/1.21.1/README.md). The [historical archive](archive/README.md) keeps earlier source material; it is not loaded, not packaged, and not current API guidance.
