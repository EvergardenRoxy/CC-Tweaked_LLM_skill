# Create with Advanced Peripherals

[Artifact scope](mod-source-baseline.md) · [Create](mod-create.md) · [AP](mod-advanced-peripherals.md) · [Production](recipes-and-production.md)

## Select the correct API layer

| Layer | Provider | Examples |
|---|---|---|
| Generic capabilities | CC:T's generic handlers | `inventory`, `fluid_storage` |
| Create's own integration | Create (`ComputerBehaviour`) | Motion, Display Link, logistics, trains |
| Extra Create capabilities | AP's Create integration | Basin, blaze burner, fluid tank, filter and scroll settings |

The reviewed AP jar adds five groups of generic methods. Its internal ID `advancedperipherals:basin` is not the peripheral type; the type is **`basin`**. Which methods a block finally has depends on how Create and AP register them, so do not promise that every Create block offers all layers at once.

Check `getType`, `hasType`, and `getMethods` on the selected network name. The fields returned by `info` differ per device.

## AP-added contracts

| Added type | Methods | Meaning |
|---|---|---|
| `basin` | `inputTanks()`, `outputTanks()` | Input and output fluids listed separately; no recipe progress |
| `blaze_burner` | `info()` | fuelType, heatLevel, remainingBurnTime, isCreative |
| `fluid_tank` | `info()` | Controller size, capacity, fluid, boiler; boiler includes active, supply, activeHeat, passiveHeat, engines |
| `filtering_behaviour` | `getFilter()`, `setFilter([table])` | Create's own filter format; returns true, or false and a reason, and may raise an error |
| `scroll_behaviour` | `getScrollValue()`, `setScrollValue(integer)` | Meaning and limits depend on the block; the setter returns nothing; not always RPM |

These methods run on the main thread, so even reads yield. Heat or fluid being present does not prove a recipe completed.

## CreateFilter is a distinct schema

`getFilter()` can return nil. Filter tables include `type`, optional behavior settings `count`/`upTo`, and type-specific data:

| Type | Shape | Boundary |
|---|---|---|
| `item` | `item={name="minecraft:iron_ingot"}` | Writing back a table you read does not necessarily reproduce the same filter |
| `list` | filters, blacklist, ignoreNBT | Nested CreateFilters; may require the matching physical filter item |
| `attribute` | mode, attributes | Use only the supported mode and attribute values |
| `package` | address | Requires a package filter item |

`setFilter(nil)` clears the filter. The block limits `count`. If the physical filter item is the wrong kind, the call returns false with a reason; do not throw away the user's filter item to get around it.

This format is neither AP's ItemFilter nor the Stock Ticker's `_requestCount` filter; convert explicitly between them.

## Derive the production controller

Follow [effective recipes and production control](recipes-and-production.md) for precision mechanisms and similar jobs. The default ingredients, loop count, weights, and failure outputs in the jar are only a reference; the controller must use the current pack's confirmed recipe. No fixed loop count or success rate is a pass criterion for every installation.

The earlier test with one work surface and a shared deployer shows how to feed extra inputs in stages; it does not require that layout. Before automating, confirm how progress is read, leftovers of extra inputs, actual transfer counts, output IDs, and the allowed way to pause.

Use one task for all material actions, a responsive listener with a bounded queue, and separate workers for reading and display. If chat replies can wait on a cooldown, keep them in a bounded queue with a defined outcome when it fills. A sent chat message, an inventory reading, and a display update are not production results.

The native monitor's lack of Chinese does not apply to mod displays and chat. Use AP's `utf8` option or JSON path and Create's byte-table path after confirming them on the installed versions. Test one short message and a multi-line display before building the whole UI.

## Joint acceptance

Cover the exact methods and event layouts; nil, false, and error results; a realistic cooldown and unique request IDs; the full configured sequence and actual delivered output; unexpected output; shortages and full destinations; partial transfers; disconnection; and interruptions around the last processing step and saving.

Keep the real adapters in fault tests. A scripted fixture or an old passing game test does not prove that new mod jars or the current recipes work in Minecraft.
