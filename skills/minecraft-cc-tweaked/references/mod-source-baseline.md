# Reviewed mod artifacts and scope

[Core](../SKILL.md) · [Create](mod-create.md) · [Advanced Peripherals](mod-advanced-peripherals.md)

The mod guides describe specific **reviewed jar files**, identified by hash, not every release with the same version number. They are references for Minecraft 1.21.1 / NeoForge, not proof that a user's server behaves the same way.

| Artifact | SHA-256 | Metadata requirements |
|---|---|---|
| Create 6.0.10 | `ef87fe5709f1ba1f5b8bb20a2925b5afb4669e178fd6d8bf10c167759eefe37a` | NeoForge >=21.1.219; Ponder >=1.0.82; client Flywheel 1.x |
| Advanced Peripherals 1.21.1-0.8.2a | `1bf3e11a1aea4cb4ab024d2fd43261d02565c304a705c6a379e7ebfa4c2d277e` | NeoForge >=21.1.238; CC:T >=1.119.0 |

AE2, Refined Storage, Mekanism, MineColonies, and other integrations are optional; having these two mods does not mean those are installed.

## Evidence layers

- Reading the class files directly lists `LuaFunction` declarations, aliases, main-thread annotations, and inheritance, without running the jars.
- Selected behavior was checked by decompiling with CFR and `javap`. Decompiled code is a reconstruction, not the original Java source.
- Recipe JSON inside a jar gives only that jar's default recipes. Datapacks, scripts, configuration, and the server's loaded recipes can replace them. Follow [recipe-driven production](recipes-and-production.md) before feeding materials.
- Scripted CC:T tests exercise the documented Lua adapters; they do not run the Java mods, process materials, or render displays.
- Earlier in-game observations apply to that installation. A matching version number does not carry them over to a different jar.

The generated [Create](mod-create-api.md) and [AP](mod-advanced-peripherals-api.md) indexes contain 113 and 369 annotated method declarations respectively, across 20 and 62 classes. These include returned objects, parent classes, plugins, and optional integrations; no single peripheral has all 482. Java class names are not peripheral type names, and Java parameters injected by CC:T (such as the computer context) are not Lua arguments.

## Compatibility differences that matter

The reviewed AP jar uses snake_case types such as `chat_box`, an options table for sending chat, a chat event with the UUID first, `getPlayer`, and `scanBlocks`. Older AP versions used other type names, positional arguments, event order, and method names. Choose an adapter from the actual `getMethods` result and verified contracts, not from a version string alone.

Defaults in the jar, such as cooldowns, ranges, or recipe chances, are reference values only. Read the actual configuration and observe the behavior. Do not set a real cooldown to zero or replace a recipe just to make a test pass.

The installed skill is self-contained. Audit files and historical originals stay in the source repository and are not needed to use these guides.
