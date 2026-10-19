# Create with Advanced Peripherals

[Artifact scope](mod-source-baseline.md) · [Create](mod-create.md) · [AP](mod-advanced-peripherals.md) · [Production](recipes-and-production.md)

## Select the correct API layer

| Layer | Provider | Examples |
|---|---|---|
| Generic capabilities | CC:T and exposed block handlers | `inventory`, `fluid_storage` |
| Native Create | Create ComputerBehaviour | Motion, DisplayLink, logistics, trains |
| Additional Create capabilities | AP Create integration | Basin, burner, tank, filtering and scroll behaviors |

The reviewed AP integration registers five GenericSource groups. An internal ID such as `advancedperipherals:basin` differs from the added peripheral type **`basin`**. Dedicated/native registration and generic-source priority can affect the final method set; do not promise every Create block exposes all layers simultaneously.

Inspect `getType`, `hasType`, and `getMethods` on the selected network name. A method named `info` has device-specific fields, not one universal schema.

## AP-added contracts

| Added type | Methods | Meaning |
|---|---|---|
| `basin` | `inputTanks()`, `outputTanks()` | Separate input/output fluid entries; no recipe-progress API |
| `blaze_burner` | `info()` | fuelType, heatLevel, remainingBurnTime, isCreative |
| `fluid_tank` | `info()` | Controller size, capacity, fluid, boiler; boiler includes active, supply, activeHeat, passiveHeat, engines |
| `filtering_behaviour` | `getFilter()`, `setFilter([table])` | Create-specific filter protocol; true or false/reason, and possible exception |
| `scroll_behaviour` | `getScrollValue()`, `setScrollValue(integer)` | Actual behavior's meaning/limits; void setter, not universally RPM |

These reviewed methods are main-thread. Reading state can yield too. Heat/fluid availability is not proof a recipe completed.

## CreateFilter is a distinct schema

`getFilter()` can return nil. Filter tables include `type`, optional behavior settings `count`/`upTo`, and type-specific data:

| Type | Shape | Boundary |
|---|---|---|
| `item` | `item={name="minecraft:iron_ingot"}` | Component update protocol is not necessarily a blind read/write round trip |
| `list` | filters, blacklist, ignoreNBT | Nested CreateFilters; matching physical filter item may be required |
| `attribute` | mode, attributes | Use actual supported enums/codecs |
| `package` | address | Requires suitable package-filter item |

`setFilter(nil)` clears the filter. Count is constrained by the underlying behavior. A physical filter-type mismatch may be a business rejection; do not discard the user's filter item to bypass it.

This schema is not AP ItemFilter and not StockTicker's `_requestCount` filter. Translate explicitly if connecting subsystems.

## Derive the production controller

Use [effective recipes and production control](recipes-and-production.md) for precision mechanisms and all similar jobs. The bundled ingredient list, repetitions, weights, and failure results are only a reference; the controller must use the current pack's confirmed profile. No fixed loop count or success probability is an acceptance criterion for every installation.

The previous single-work-surface/shared-deployer test illustrates staged auxiliary feeding; it does not mandate that topology. Confirm workpiece progress, auxiliary leftovers, actual transfer counts, output identities, and authorized pause mechanism before automating.

Use one material-action owner, a responsive listener with bounded acceptance, and observation/render workers. If replies can wait on cooldown, give them bounded pending work and an explicit outcome policy. Successful chat submission, inventory sampling, and display submission are separate from production settlement.

Native monitor glyph restrictions do not apply automatically to mod displays/chat. Use the reviewed AP options or JSON path and Create byte-table path only after confirming the actual binary contracts. Test one short message and a multiline display before building the complete UI.

## Joint acceptance

Cover exact methods/event layouts; nil/false/exception boundaries; realistic cooldown and unique request IDs; full configured sequence and actual delivered outputs; unknown output; shortages/full destinations; partial transfers; disconnection; and the relevant final-processing/persistence windows.

Preserve the real adapters in fault tests. A scripted fixture or an old passing game test does not prove the newly supplied Java binaries or current effective recipes work in Minecraft.
