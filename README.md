[简体中文](README.zh-CN.md)

# CC: Tweaked LLM Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI-Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](#ai-production-disclosure)

> An Agent Skill that helps Claude and other LLMs write, review, and debug Minecraft **CC: Tweaked (ComputerCraft)** Lua programs correctly.

[CC: Tweaked](https://tweaked.cc) is the modern fork of ComputerCraft: programmable computers, turtles, and peripherals inside Minecraft. Its Lua environment is not desktop Lua: it runs on Cobalt (Lua 5.2), is driven by events and yielding, addresses peripherals by side or network name, and makes turtles burn fuel. Models that rely on old tutorials or memory invent functions, mix up `:` and `.`, lose events, or write Lua 5.3 syntax that does not compile.

This repository turns the execution model, APIs, peripherals, turtles, networking, design patterns, and troubleshooting into guidance an agent can follow. Core API contracts come from [tweaked.cc](https://tweaked.cc); the user's installed mods, server configuration, and effective recipes decide how that guidance applies.

**Design philosophy: break the task down, agree on the goal, then write code.** The skill steers the agent toward the simplest solution that works, from existing game mechanics and ROM programs to a short script or a full application. It reuses what the user already said, implements explicit requests directly, and asks only when a missing fact would change the design. Interfaces, logging frameworks, and authentication are added only when the task needs them.

**Teach the reasoning, not just the answer.** The skill explains constraints, structure choices, failure modes, and composable patterns: a responsive input listener beside yielding workers, bounded queues, checking that an action actually happened, recipe profiles, and reconciliation after a restart. Every example states where it stops applying; a familiar recipe or one passing test is never treated as a rule for every installation.

<a id="ai-制作声明"></a>
<a id="ai-production-disclosure"></a>

> [!IMPORTANT]
> **AI production disclosure: CC: Tweaked LLM Skill uses generative AI to assist with content creation, code validation, and documentation.** AI-generated or modified content is reviewed and verified by the project maintainer, who retains final responsibility for its maintenance.

> **Current release: [v1.3.0](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/tag/v1.3.0)** (2026-10). The skill is written in English: a core `SKILL.md` plus 26 topic references, with Create and Advanced Peripherals guides tied to the reviewed jars and production control derived from the modpack's effective recipes. The source tree also contains unreleased changes; see the [release notes](RELEASE_NOTES.md) ([中文](RELEASE_NOTES.zh-CN.md)).

---

## What it can do

| Scenario | Example request |
|---|---|
| Write a program | “Count the items in my wired chests and show the totals on a monitor.” |
| Turtle automation | “Write a tunnel-mining program with a size limit, fuel checks, unloading, and recovery after an interrupted move.” |
| Networking and remote control | “Use rednet to switch a redstone output and report whether the command completed.” |
| Mod machines and factories | “Control this production line with the actual Create peripherals and the recipes in my pack.” |
| Dashboards and touch interfaces | “Build a monitor panel that keeps responding to touches while it polls inventories.” |
| Code review | “Check this ComputerCraft program for wrong API calls and item-count mistakes.” |
| Troubleshooting | “Explain this `attempt to index nil` or `Too long without yielding` error.” |
| Testing and live diagnosis (with compatible tools) | “Run the program in cct-run and tell me which results came from fixtures and which from the game.” |

A delivered answer explains the approach, the devices and names it needs, the code, how to install and run it, and how it was verified. Detail scales with the task: a small fix does not get an application framework.

## Skill contents

The skill uses **progressive loading**. `SKILL.md` (204 lines) holds the workflow, rules, execution model, quick reference, common mistakes, delivery format, reference map, and delivery checklist. The agent reads the 26 topic references only when a task needs them. Create and Advanced Peripherals contracts are kept apart from core CC:T and tied to the specific jars that were reviewed.

The references cover APIs, peripherals, events, state and recovery, recipes, turtles, networking, UI and text encoding, application engineering, security, patterns, testing, and troubleshooting. The mod guides describe Create 6.0.10 and Advanced Peripherals 1.21.1-0.8.2a on Minecraft 1.21.1 / NeoForge. Optional integrations (AE2, Refined Storage, Mekanism, and others) need those mods installed.

See the [contents overview](CONTENTS.md) and the [full reference map](skills/minecraft-cc-tweaked/SKILL.md#reference-map). Historical source material is kept in `archive/`, outside the installed skill and the prompt pack.

## Installation

The skill follows the open [Agent Skills](https://agentskills.io) format. Install the whole `skills/minecraft-cc-tweaked/` folder, **including `references/`**, into your client's skill directory. In Claude Code:

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

For clients that import an archive, download [CCT_prompt_pack.zip](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/CCT_prompt_pack.zip); its root contains `SKILL.md` and `references/`. Check it against the release's [SHA256SUMS](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/SHA256SUMS).

[Installation and upgrades](INSTALL.md) covers directory and archive installs, including Codex. Paths and support differ between clients; follow your client's documentation. Upgrade by replacing the whole folder so old and new references are never mixed.

## Usage

After installation, ask your agent to use the skill for CC:T work; whether it is picked up automatically depends on the client. Where relevant, provide:

- The CC:T version (run `print(_HOST)` in the `lua` prompt), Minecraft version, loader, and relevant mod versions.
- The device type, peripheral layout or network names, and the result you want.
- Existing code and the complete error message, including file and line.
- For production lines: the recipes as they currently work in your pack, and which machine actions the program may take.

### Optional companion: cct-run

[cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) is a separate test runtime and MCP server (`cct-run mcp`). It runs programs on real CC:T code outside Minecraft, emulates core peripherals, and returns scripted responses for mod peripherals, so an agent can check errors, traces, and screens before delivering.

With a compatible cct-live installation and your permission, an agent can also diagnose a chosen in-game computer. The tools are optional: the skill itself installs no mods and connects to no game. See the [testing guide](skills/minecraft-cc-tweaked/references/testing.md) for what each kind of test can and cannot prove.

### Test evidence

| Check | Result and scope |
|---|---|
| Static checks | 14 Lua blocks: Lua 5.2 syntax, selected official API names, and global variables |
| Validator regressions | 10 cases covering prose, links, code fences, Unicode data, and offline mode |
| Reliability examples (v1.3.0) | 22 assertions plus dashboard input handling in cct-run / CC:T 1.120.2 |
| Mod adapters (v1.3.0) | 17 scripted assertions and trace checks; the Java mods are not executed |
| Prompt pack | 27 Markdown files; paths, CRCs, and byte equality with the source are checked |

Earlier joint tests shaped the recovery, event, and encoding guidance, but their timings, layouts, permissions, and recipe values do not guarantee performance or compatibility elsewhere. See the [mod evidence](docs/mod-evidence/1.21.1/README.md) and the [release notes](RELEASE_NOTES.md) for scope.

## Accuracy and validation

- [`scripts/validate_skill.py`](scripts/validate_skill.py) compiles every Lua block with Lua 5.2, checks selected core API members against [tweaked.cc](https://tweaked.cc), and catches global-variable and dot/colon mistakes. Compiling on the host is not full Cobalt compatibility testing.
- The mod guides keep class-file/decompilation evidence, scripted adapter tests, and real game observations apart. A method name in a generated index says nothing about its arguments or whether it exists in a given game.
- The server's current data and configuration can override bundled recipes and defaults. Discover the actual methods and check the relevant behavior before moving materials.
- [GitHub Actions](.github/workflows/validate.yml) validates the skill and builds the prompt pack on every push and pull request. Static checks and scripted fixtures do not prove game physics, rendering, or every recovery path.

Run validation and packaging with Python and a Lua 5.2 compiler:

```bash
python3 scripts/validate_skill.py
python3 scripts/test_validator.py
python3 scripts/package_skill.py
```

The first validation run caches the official API pages in `.cache/`; later runs can use `--offline`. With a compatible cct-run installed, run the examples extracted from the references:

```bash
python3 scripts/test_examples.py --cct-run /absolute/path/to/cct-run
python3 scripts/test_mod_examples.py --cct-run /absolute/path/to/cct-run
```

## Acknowledgments

- [cc-tweaked/CC-Tweaked](https://github.com/cc-tweaked/CC-Tweaked) and [tweaked.cc](https://tweaked.cc): the mod and its official documentation.
- [dan200/ComputerCraft](https://github.com/dan200/ComputerCraft): the original ComputerCraft.
- [SuperFactoryManager_LLM_skill](https://github.com/EvergardenRoxy/SuperFactoryManager_LLM_skill): the model for this repository's structure.

## License

[MIT](LICENSE) © 2026 EvergardenRoxy

This repository contains guidance, evidence records, and validation scripts. It does not include the CC:T mod itself; CC:T and the other projects mentioned keep their own licenses.
