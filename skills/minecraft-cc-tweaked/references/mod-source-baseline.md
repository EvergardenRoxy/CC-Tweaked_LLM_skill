# Reviewed mod artifacts and scope

[Core](../SKILL.md) · [Create](mod-create.md) · [Advanced Peripherals](mod-advanced-peripherals.md)

These guides describe reviewed **binary artifacts**, not every release with the same label. They are reference profiles for Minecraft 1.21.1 / NeoForge, not proof that a user's server exposes the same behavior.

| Artifact | SHA-256 | Metadata requirements |
|---|---|---|
| Create 6.0.10 | `ef87fe5709f1ba1f5b8bb20a2925b5afb4669e178fd6d8bf10c167759eefe37a` | NeoForge >=21.1.219; Ponder >=1.0.82; client Flywheel 1.x |
| Advanced Peripherals 1.21.1-0.8.2a | `1bf3e11a1aea4cb4ab024d2fd43261d02565c304a705c6a379e7ebfa4c2d277e` | NeoForge >=21.1.238; CC:T >=1.119.0 |

AE2, Refined Storage, Mekanism, MineColonies, and other integrations are optional; having these two jars does not imply those mods are installed.

## Evidence layers

- Direct class-file parsing identifies `LuaFunction` declarations, aliases, main-thread annotations, and inheritance without executing the jars.
- Selected Java implementation semantics were checked through CFR decompilation and `javap`. These are reconstructed implementation evidence, not supplied original Java source.
- Bundled resource JSON establishes only the artifact's baseline recipes. Datapacks/scripts/configuration and the effective server recipe manager can supersede it. Follow [recipe-driven production](recipes-and-production.md) before feeding materials.
- Scripted CC:T tests exercise the documented Lua adapters, not Java mod execution or real processing/rendering.
- Historical game observations concern their original installation. They cannot validate a newly uploaded binary by version label alone.

The generated [Create](mod-create-api.md) and [AP](mod-advanced-peripherals-api.md) indexes contain 113 and 369 annotated method declarations respectively, across 20 and 62 classes. These include returned objects, parents, plugins, and optional integrations; they are not 482 methods available on each computer. Java implementation names are not peripheral type names, and injected Java parameters are not automatically Lua arguments.

## Compatibility differences that matter

The reviewed AP artifact uses snake_case types such as `chat_box`, options-table chat sending, a UUID-first chat event, `getPlayer`, and `scanBlocks`. Older notes/test installations used other types, positional arguments, event order, and method names. Select an adapter from actual methods plus verified contracts, not a version string alone.

Artifact defaults such as cooldowns, ranges, or bundled probabilities are reference values. Read actual configuration and observe the relevant boundary. Do not relax a real cooldown to zero or replace a recipe just to make a test pass.

The installed skill is self-contained. Development audit files and historical originals are kept separately in the source repository and are not prerequisites for using these guides.
