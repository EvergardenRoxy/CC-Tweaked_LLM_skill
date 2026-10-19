[简体中文](README.zh-CN.md)

# CC: Tweaked LLM Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![AI Assisted](https://img.shields.io/badge/AI-Claude%20Code-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](#ai-production-disclosure)

> An Agent Skill that helps Claude and other LLMs correctly write, review, and debug Minecraft **CC: Tweaked (ComputerCraft)** Lua programs.

[CC: Tweaked](https://tweaked.cc) is the modern ComputerCraft fork: programmable computers, turtles, and peripherals inside Minecraft. Its Lua environment differs from a desktop interpreter: Cobalt, events and yielding, peripherals addressed by side or network name, and turtle fuel. Old tutorials and remembered APIs can lead models to invent functions, confuse `:` with `.`, miss events, or generate unsupported Lua syntax.

This repository organizes the execution model, APIs, peripherals, turtles, networking, design patterns, and troubleshooting into guidance an agent can follow. Core API contracts come from [tweaked.cc](https://tweaked.cc); installed capabilities, mod implementations, server configuration, and effective recipes determine how that guidance applies to the current environment.

**Design philosophy: break down the task, establish the goal, and teach the reasoning.** Choose the simplest adequate approach—from existing game mechanics and ROM programs to a short script or a larger application. Reuse supplied requirements and proceed with authorized work; ask when missing information changes correctness or scope. Add interfaces, logging frameworks, or authentication only when the task needs them.

**Teach how to derive a program, not just how to imitate one.** The skill covers constraints, architecture choices, failure modes, and composable patterns: responsive input with yielding workers, bounded queues, verified effects, recipe profiles, and restart reconciliation. Examples have explicit adaptation boundaries; a familiar recipe or one successful test is not a universal control specification.

<a id="ai-制作声明"></a>
<a id="ai-production-disclosure"></a>

> [!IMPORTANT]
> **AI production disclosure: CC: Tweaked LLM Skill uses generative AI to assist with content creation, code validation, and documentation.** AI-generated or modified content is reviewed and verified by the project maintainer, who retains final responsibility for its maintenance.

> **Current version: [v1.3.0](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/tag/v1.3.0)** (2026-10). The active skill is now English, with a compact core and 26 references. This release incorporates reliability lessons and artifact-scoped Create/AP guides, and derives production control from the current modpack's effective recipes. See the [English release notes](RELEASE_NOTES.md) or [中文发行说明](RELEASE_NOTES.zh-CN.md).

---

## What it can do

| Scenario | Example request |
|---|---|
| Write a program | “Count items across my wired inventories and show the totals on a monitor.” |
| Turtle automation | “Design a bounded tunnel-mining program with fuel checks, unloading, and interrupted-movement recovery.” |
| Networking and remote control | “Use rednet to control a redstone output and report whether the command completed.” |
| Mod machines and factories | “Use the actual Create peripherals and effective recipes to control this production line.” |
| Dashboards and touch interfaces | “Build a monitor panel that stays responsive while polling inventories.” |
| Code review | “Check this ComputerCraft program for incorrect APIs and transfer accounting.” |
| Troubleshooting | “Explain this nil-value error or `Too long without yielding` failure.” |
| Testing and live diagnosis, with compatible tools | “Run the program in cct-run and distinguish fixture results from game observations.” |

Deliveries should explain the approach, required devices and names, program changes, launch steps, and relevant verification. Detail scales with the task; a small fix does not need a large application framework.

## Skill contents

The skill uses **progressive loading**: the 97-line `SKILL.md` contains the workflow, evidence boundaries, runtime rules, and reference map; the agent reads the 26 topic references as needed. Create and Advanced Peripherals contracts are separated from core CC:T and scoped to the reviewed artifacts.

Topics include APIs, peripherals, events, recovery, recipes, turtles, networking, UI/text, application engineering, security, patterns, and testing. The mod guides cover Create 6.0.10 and Advanced Peripherals 1.21.1-0.8.2a for Minecraft 1.21.1 / NeoForge. Optional integrations require their respective installed mods.

See [contents](CONTENTS.md) and the [complete reference map](skills/minecraft-cc-tweaked/SKILL.md#reference-map). Historical originals are preserved in `archive/`, outside the installed skill and prompt pack.

## Installation

The skill follows the open [Agent Skills](https://agentskills.io) format. Install the complete `skills/minecraft-cc-tweaked/` folder, **including `references/`**, in your client's supported skill directory. For Claude Code:

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

For archive-based clients, download [CCT_prompt_pack.zip](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/CCT_prompt_pack.zip); its root contains `SKILL.md` and `references/`. Verify it against the release's [SHA256SUMS](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/SHA256SUMS).

See [installation and upgrades](INSTALL.md) for directory/import guidance, including Codex. Client support and paths vary; use the installed client's documented location. Upgrade the complete skill to avoid mixing old and new references.

## Usage

After installation, ask your agent to use the skill for CC:T work. Automatic discovery depends on the client. When relevant, provide:

- CC:T version (`print(_HOST)` inside the Lua interpreter), Minecraft version, loader, and relevant mod versions.
- Device kind, peripheral layout or network names, and the intended result.
- Existing code and complete errors, including file and line.
- For production, current effective recipe evidence and the permitted machine actions.

### Optional companion: cct-run

[cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) provides a separate test runtime and MCP server (`cct-run mcp`). It can run programs on CC:T outside Minecraft, model core peripherals, and script mod-boundary responses. Agents can inspect errors, traces, and screens before delivery.

With a compatible cct-live installation and authorized access, an agent can also diagnose a specified in-game computer. Test tooling is optional: the skill itself installs no mods or game connection. See [testing guidance](skills/minecraft-cc-tweaked/references/testing.md) for evidence layers and live-work boundaries.

### Test evidence

| Current verification | Result and scope |
|---|---|
| Static checks | 12 Lua blocks; Lua 5.2 syntax, selected official API names, and globals |
| Validator regressions | 10 cases covering prose, links, fences, Unicode data, and offline behavior |
| Reliability examples | 22 assertions plus dashboard input handling in cct-run / CC:T 1.120.2 |
| Mod adapters | 17 scripted assertions and trace checks; no Java mod execution |
| Prompt pack | 27 active Markdown files; paths, CRCs, and source-byte equality checked |

Historical joint tests informed the recovery/event/encoding guidance, but their timings, layouts, permissions, and recipe values are not universal performance or compatibility guarantees. See [mod evidence](docs/mod-evidence/1.21.1/README.md) and [release notes](RELEASE_NOTES.md) for scope.

## Accuracy and validation

- [`scripts/validate_skill.py`](scripts/validate_skill.py) compiles active Lua blocks with Lua 5.2, checks selected core API members against [tweaked.cc](https://tweaked.cc), and catches global-variable and dot/colon mistakes. Host compilation is not complete Cobalt compatibility testing.
- The mod guides distinguish class-file/decompilation evidence, scripted adapter tests, and actual game observations. Names in a generated index do not establish argument contracts or live availability.
- Current server data/configuration can override bundled recipes and defaults. Discover actual methods and verify the relevant behavior before controlling materials.
- [GitHub Actions](.github/workflows/validate.yml) validates the skill and builds the prompt pack on pushes and pull requests. Static checks and scripted fixtures do not prove game physics, rendering, or every recovery window.

Run validation and packaging with Python and a Lua 5.2 compiler:

```bash
python3 scripts/validate_skill.py
python3 scripts/test_validator.py
python3 scripts/package_skill.py
```

The first validation run caches official API pages in `.cache/`; subsequent runs can use `--offline`. With a compatible cct-run installation, run the extracted examples:

```bash
python3 scripts/test_examples.py --cct-run /absolute/path/to/cct-run
python3 scripts/test_mod_examples.py --cct-run /absolute/path/to/cct-run
```

## Acknowledgments

- [cc-tweaked/CC-Tweaked](https://github.com/cc-tweaked/CC-Tweaked) and [tweaked.cc](https://tweaked.cc): the mod and official documentation.
- [dan200/ComputerCraft](https://github.com/dan200/ComputerCraft): the original ComputerCraft.
- [SuperFactoryManager_LLM_skill](https://github.com/EvergardenRoxy/SuperFactoryManager_LLM_skill): an influence on the repository structure.

## License

[MIT](LICENSE) © 2026 EvergardenRoxy

This repository contains guidance, evidence records, and validation scripts; it does not include the CC:T mod itself. CC:T and other referenced projects retain their own licenses.
