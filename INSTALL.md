# Installation and upgrades

[README](README.md) · [Contents](CONTENTS.md)

Install the **complete** `skills/minecraft-cc-tweaked/` folder, including `SKILL.md` and `references/`, using your agent client's supported skill directory or import UI. Do not install only the core file: its topic references are required.

## Directory-based clients

For clients supporting Agent Skills, copy the directory into their documented skill location. For example, Codex project skills can live at `.agents/skills/minecraft-cc-tweaked/`; user-level locations and other clients vary. Follow the installed client's current documentation rather than assuming every client searches the same paths.

For Claude Code marketplace installation, add `EvergardenRoxy/CC-Tweaked_LLM_skill` as a marketplace and install `minecraft-cc-tweaked@cct-llm-skills` using the client's plugin UI/commands. The repository preserves its existing marketplace layout.

## ZIP import

Use `CCT_prompt_pack.zip` when the client supports uploading a skill archive. Its root contains `SKILL.md` and `references/`. If the client requires a folder rather than this archive layout, extract those files into a folder named `minecraft-cc-tweaked` and install it using that client's instructions.

The pack includes the active English skill only. Development audits, historical Chinese source records, raw jars, and test tooling are not runtime dependencies.

## Upgrade safely

Back up any locally customized installed skill. Stage the complete new folder, compare customizations, and replace the old installation as one coherent version using a recoverable local procedure. Do not overlay selected new references onto an old core or leave stale references active.

Do not copy development `archive/` records into the active skill directory. Check that the client discovers the skill and can resolve a reference after installation. Loading the skill does not install Minecraft mods, connect a live computer, or grant permission to control a world.
