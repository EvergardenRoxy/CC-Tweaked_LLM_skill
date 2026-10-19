[简体中文](README.zh-CN.md)

# CC: Tweaked LLM Skill

A programming skill that helps AI agents design, write, review, and debug Minecraft **CC: Tweaked (ComputerCraft)** Lua programs for computers, turtles, peripherals, and mod automation.

**Current release: [v1.3.0](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/tag/v1.3.0).** The active skill and reference documents are written in English.

## What it covers

- Core CC:T APIs, peripheral discovery, inventories, fluids, energy, redstone, and turtle programming.
- Responsive event handling, bounded work queues, persistent state, interrupted-action recovery, and observed completion.
- Terminal/monitor interfaces, text encoding, rednet, GPS, HTTP, and WebSockets.
- Create motion, stress, displays, logistics, packaging, and trains.
- Advanced Peripherals chat, sensors, player inventory, storage bridges, optional extensions, and its Create integration.
- Recipe-driven automation based on the **current modpack's effective recipes**, rather than assumed ingredients, loop counts, or success rates.

The mod guides describe reviewed Create 6.0.10 and Advanced Peripherals 1.21.1-0.8.2a artifacts for Minecraft 1.21.1 / NeoForge. Check the actual methods, configuration, and effective recipes before applying their examples. Optional integrations require their respective installed mods.

## Install

Download [CCT_prompt_pack.zip](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases/download/v1.3.0/CCT_prompt_pack.zip) from the release and import it into a client that supports skill archives. The ZIP root contains `SKILL.md` and `references/`.

For directory-based clients, install the complete [`skills/minecraft-cc-tweaked`](skills/minecraft-cc-tweaked/SKILL.md) directory, including `references/`, in the client's supported skill location. For example, Codex project skills can use `.agents/skills/minecraft-cc-tweaked/`.

For Claude Code, add this repository as a marketplace and install `minecraft-cc-tweaked@cct-llm-skills` through the plugin interface.

See [installation and upgrades](INSTALL.md) for details. Replace the complete skill when upgrading so that the core and references stay consistent.

## Use

Ask your agent to use the skill for a CC:T task. Provide relevant game/mod versions, device layout, existing code or errors, and the intended result when available. For example:

- “Review this inventory controller for missed events and incorrect transfer counts.”
- “Build a Create production controller using the recipes and peripherals in this modpack.”
- “Diagnose why this Advanced Peripherals chat command fails after a restart.”

The skill is programming guidance. It does not install Minecraft mods or include a game connection/testing runtime. Agents can use compatible tools when available and should distinguish simulated checks from actual game observations.

## Documentation

| Document | Purpose |
|---|---|
| [Skill entry point](skills/minecraft-cc-tweaked/SKILL.md) | Workflow and complete reference map |
| [Contents](CONTENTS.md) | Topic overview |
| [Installation](INSTALL.md) | Installation layouts and upgrades |
| [Release notes](RELEASE_NOTES.md) | v1.3.0 changes and verification |
| [Mod evidence](docs/mod-evidence/1.21.1/README.md) | Reviewed artifacts and reproducible method indexes |

Historical originals remain in `archive/` for provenance; they are excluded from the active skill and prompt pack.

## Development

```bash
python3 scripts/validate_skill.py
python3 scripts/test_validator.py
python3 scripts/package_skill.py
```

Validation requires a Lua 5.2 compiler and official API pages cached from tweaked.cc. Use `--offline` after the cache has been populated. With a compatible [cct-run](https://github.com/EvergardenRoxy/CC-Tweaked_MCP) installation, also run:

```bash
python3 scripts/test_examples.py --cct-run /absolute/path/to/cct-run
python3 scripts/test_mod_examples.py --cct-run /absolute/path/to/cct-run
```

The extracted-example tests exercise CC:T runtime behavior and scripted mod boundaries; they do not execute the supplied Java mods or verify Minecraft processing/rendering. CI validates the skill and builds the prompt pack.

## License

See [LICENSE](LICENSE).
