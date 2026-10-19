# AP extensions and optional integrations

[AP](mod-advanced-peripherals.md) · [Artifact scope](mod-source-baseline.md) · [Index](mod-advanced-peripherals-api.md)

This page points to AP features; it does not mean every addon must be installed. Classes in the index can be returned objects, plugins, or optional integrations. Before acting, confirm the feature is registered, which device form has it, permissions, costs, and argument formats.

## Turtles, pocket devices, and automata

Block, pocket, and turtle versions of a peripheral can differ in owner, fuel, what "front" means, and available methods. AP turtle upgrades are wrapped as peripherals; their methods are not added to `turtle.*`.

- `compass.getFacing()` returns the facing direction.
- `chunky.getRadius()` returns the configured chunk-loading radius in chunks; it does not keep a whole factory or route loaded.
- FuelAbility methods (`getFuelLevel`, `getMaxFuelLevel`, consumption rate) follow AP's rules and differ from `turtle.getFuelLevel`.
- An automata core's type decides its abilities; weak, end, husbandry, and overpowered cores have different method sets.

| Plugin area | Examples | Confirm before use |
|---|---|---|
| Blocks | dig/use/update/place | Target direction, cost, protected areas, effect on materials |
| Observation | lookAtBlock/lookAtEntity | Range and returned fields |
| Animals | inspect/search/use | Which animal is targeted, tools, conditions |
| Capture/release | captureAnimal/releaseAnimal | Whether one is already carried; interruption |
| Drops | scan/collect | Scanning is not collecting; space and partial success |
| Energy/souls | chargeTurtle/feedSoul | Resource type and cost in survival |
| Teleportation | save/list/delete points, warp, estimate cost, portals | Dimension, fuel, permission, recovery after failure |

Never call digging, capture, teleport, or point deletion just to see whether it works. A CC:T simulator cannot test AP movement or teleportation.

## Saddle and smart rail

`saddle` capture, release, and rider methods change state and may have cooldowns. `smart_rail` manages vanilla minecarts, not Create trains. Read the actual state names and configuration instead of guessing from numbers.

## Smart glasses

The global `smartglasses` API exists only while the glasses are bound and worn; it covers the owner, equipment, and supported operations. Do not define a fake global of that name when it is missing.

The `smart_glasses` peripheral returns module objects through `getModules`, `hasModule`, and `getModule`; take module IDs from those results. The overlay module manages text, rectangle, line, item, block, and sphere objects, each with its own coordinate and property methods. Batch changes, then update explicitly unless auto-update is confirmed. It is not a CC monitor.

Keyboard, night-vision, and other modules have their own methods. Placement on screen, input events, view and world coordinates, fonts, and rendering must be checked in the game.

## Optional integrations

| Installed dependency | Domain | Routing/boundary |
|---|---|---|
| Create | Basin/burner/tank/filter/scroll | [Create with AP](mod-create-ap.md) |
| AE2 / Refined Storage | Storage and crafting | [AP storage](mod-advanced-peripherals-storage.md) |
| Mekanism | Chemicals and radiation | Without Mekanism, calls report "unsupported" instead of zero |
| MineColonies | Colony, citizen, building, work order, request, research data | Check colony membership, range, and access separately |
| Curios | Player accessory slots | Not the same as vanilla slot numbers |
| Powah / DimStorage | Energy and dimensional storage | Check that the integration is loaded |
| Vanilla beacon/note block | Beacon level and effects; note changes and playing | Main-thread methods; check return fields |

Use only what the task needs. A class appearing in the jar or index does not mean the pack loads that dependency, or that this path was tested in a game.
