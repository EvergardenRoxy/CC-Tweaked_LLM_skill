# Installation and upgrades

[README](README.md) · [Contents](CONTENTS.md)

Install the **complete** `skills/minecraft-cc-tweaked/` folder, including `SKILL.md` and `references/`, through your agent client's skill directory or import screen. Do not install `SKILL.md` alone: it links to the topic references.

## Claude Code

Add the repository as a plugin marketplace and install the skill:

```text
/plugin marketplace add EvergardenRoxy/CC-Tweaked_LLM_skill
/plugin install minecraft-cc-tweaked@cct-llm-skills
```

## Other directory-based clients

Copy the folder into the location your client documents for Agent Skills. For example, Codex project skills can live in `.agents/skills/minecraft-cc-tweaked/`. User-level locations and other clients differ; follow your client's current documentation instead of assuming every client searches the same paths.

## ZIP import

Use `CCT_prompt_pack.zip` from the [release page](https://github.com/EvergardenRoxy/CC-Tweaked_LLM_skill/releases) when the client accepts a skill archive. Its root contains `SKILL.md` and `references/`. If the client expects a folder instead, extract those files into a folder named `minecraft-cc-tweaked` and install that.

The pack contains only the installed English skill. Development audits, historical Chinese source records, mod jars, and test tooling are not needed at runtime.

## Upgrading

1. Back up the installed skill if you customized it.
2. Prepare the complete new folder and carry over any customizations you want to keep.
3. Replace the old installation as a whole. Do not copy individual new references over an old core, and do not leave stale references in place.

Do not copy `archive/` records into the skill directory. After installing, check that the client finds the skill and can open a reference. Loading the skill does not install Minecraft mods, connect to a game, or grant permission to change a world.
