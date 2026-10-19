# AP extensions and optional integrations

[AP](mod-advanced-peripherals.md) · [Artifact scope](mod-source-baseline.md) · [Index](mod-advanced-peripherals-api.md)

This page routes capabilities; it does not require installing every addon. Annotated classes can represent returned objects, plugins, or optional integrations. Verify registration, owner/device form, permissions, costs, and argument contracts before acting.

## Turtles, pocket devices, and automata

Block, pocket, and turtle forms can differ in ownership, fuel, adjacent-side interpretation, and available methods. AP methods are not automatically `turtle.*` methods.

- `compass.getFacing()` reports facing.
- `chunky.getRadius()` reports configured chunk-loading radius. The unit is chunks; coverage is not a guarantee that an entire factory or route stays loaded.
- FuelAbility methods such as `getFuelLevel`, `getMaxFuelLevel`, and consumption-rate accessors have AP-specific semantics distinct from native turtle fuel.
- Automata tier/plugins determine available behavior. Weak/End/Husbandry/Overpowered cores are not interchangeable capability sets.

| Plugin area | Examples | Confirm before use |
|---|---|---|
| Blocks | dig/use/update/place | Relative target, cost, protection, material effects |
| Observation | lookAtBlock/lookAtEntity | Range/raycast and returned fields |
| Animals | inspect/search/use | Target selection, tools, interaction conditions |
| Capture/release | captureAnimal/releaseAnimal | Existing carried state and interrupted effects |
| Drops | scan/collect | Separate observation from collection; capacity/partial success |
| Energy/souls | chargeTurtle/feedSoul | Resource type and survival costs |
| Teleportation | save/list/delete points, warp/estimate cost, portal phases | Dimension, fuel, stage identity, authorization and recovery |

Do not probe destructive calls, capture, teleport, or point deletion just to discover capability. A core-runtime simulator does not validate AP movement/teleportation.

## Saddle and smart rail

`saddle` capture/release/rider queries are stateful and may have cooldowns. `smart_rail` cart queries and state/activation setters manage vanilla minecarts, not Create trains. Read actual state enums and configuration rather than guessing names from numeric values.

## Smart glasses

The injected `smartglasses` API depends on binding/wearing and exposes owner/equipment and supported smart equipment operations. Do not create a fake same-named global when absent.

The `smart_glasses` peripheral returns module objects via `getModules`, `hasModule`, `getModule`; take IDs from actual results. Overlay modules manage text/rectangle/line/item/block/sphere objects with their own coordinate/property methods. Batch changes and use explicit update or verified auto-update behavior. They are not CC monitors.

Keyboard/night-vision and other modules have separate contracts. Actual GUI placement, input events, eye/world coordinates, fonts, and client rendering require game verification.

## Optional integrations

| Installed dependency | Domain | Routing/boundary |
|---|---|---|
| Create | Basin/burner/tank/filter/scroll | [Create with AP](mod-create-ap.md) |
| AE2 / Refined Storage | Storage and crafting | [AP storage](mod-advanced-peripherals-storage.md) |
| Mekanism | Chemicals and radiation | Explicit unsupported result when unavailable |
| MineColonies | Colony, citizen, building, work/request/research data | Check colony membership, range, activity, and access separately |
| Curios | Player accessory slots | Do not substitute vanilla slot numbering |
| Powah / DimStorage | Energy/dimensional handlers | Verify current installed integration |
| Vanilla beacon/noteblock | Beacon state and note operations | Main-thread actions and actual schemas |

Use only domains the user's task needs. The presence of these classes in a jar/index is not evidence that the current pack loads all dependencies or that these paths were tested live.
