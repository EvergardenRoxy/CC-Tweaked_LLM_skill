# AP inventory, storage bridges, and crafting

[AP](mod-advanced-peripherals.md) · [Artifact scope](mod-source-baseline.md) · [Index](mod-advanced-peripherals-api.md) · [Recovery](state-and-recovery.md)

## Select the layer

Ordinary container transfers should use core inventory handlers where adequate. `inventory_manager` accesses a bound player's inventory; `me_bridge`/`rs_bridge` access their respective optional storage networks; Create logistics use another request model. Directions, filters, and success meanings differ.

AE2/Refined Storage/Mekanism are not implied by the supplied Create/AP pair. Verify installation, bridge connection/online state, permissions, and supported resource types. A disconnected network is an error/unknown state, not zero stock.

## AP ItemFilter

| Field | Reviewed meaning |
|---|---|
| `name` | Registry ID, or #tag where supported |
| `count` | Quantity limit; explicitly provide a positive bounded integer |
| `fromSlot`, `toSlot` | One-based indexes; not direction strings |
| `components` | Table/SNBT component patch for this version, not arbitrary legacy NBT |
| `matcher` | Current supported component match mode; verify enum/schema |
| `nbtHash` | Component-patch fingerprint in this implementation; do not assume legacy NBT compatibility |

An empty filter can match everything. Unknown resources may return nil/reason; malformed fields may throw. AP ItemFilter, CreateFilter, and StockTicker comparison filters are separate schemas.

## Inventory Manager

`getOwner()` returns **uuid, name as two values**, or no result when unbound. Verify the memory card/owner and accessibility. `list` is sparse; query hand/offhand/armor/free slots using the actual method semantics.

`importItem(fromName [, filter])` moves external inventory into the player; `exportItem(toName [, filter])` moves outward. Check actual moved counts. Some block-owner methods accept `@front`-style names relative to that **AP block**. This is not a universal direction convention for core `pushItems`, pocket devices, or every AP method.

`wrapStorageItem(slot)` returns an object bound to that storage item. Check `isValid`, `isItemStorage`/`isFluidStorage`, then its list/tanks/import/export methods. Invalidate it when the item/access context changes; it is not a permanent network peripheral.

## Bridge method families

Bridges can also expose the `storage_bridge` type. Consult the exact method set and implementation:

| Need | Reviewed family |
|---|---|
| Single resource | `getItem`, `getFluid`, `getChemical` |
| Lists | `getItems`, `getFluids`, `getChemicals` |
| Craftable resources | `getCraftableItems/Fluids/Chemicals`, `isCraftable` |
| Movement | `importItem`/`exportItem` and fluid/chemical counterparts |
| Network information | `getCells`, `getDrives`, `getStoredEnergy`, `getEnergyCapacity`, `getEnergyUsage`, `getAverageEnergyInput` |
| Capacity | Max/Used/Available storage and external variants; exact names in index |
| Tasks | `craftItem`, corresponding resource methods, `getCraftingTasks`, `getCraftingTask`, `cancelCraftingTasks`, `isCrafting` |
| Patterns | `getPatterns` with verified input/output filter schema |

Do not reuse old `listItems` or energy names. Unsupported chemical/addon operations are explicit errors, not zero quantities. ME's optional CPU-name argument must not be assumed on RS methods.

## Asynchronous work

A successful ME crafting call returns a task object, not a product count. Relevant object methods include `getId`, done/canceled/calculation/crafting/error status, debug message, requested item, elapsed time, total/progress/emitted/used/missing items, paths, final output, and `cancel`; use exact names from the index. These are returned-object methods, not bridge methods.

Persist request intent/task ID as needed. Distinguish calculation, queueing, started work, completion, and actual available/delivered product. Restart by finding old tasks and reconciling stock before requesting again. Cancellation can leave intermediate effects. ME `getCraftingCPUs` and RS `getCrafters` are separate capabilities.

Cover missing patterns/materials, offline networks, invalid filters, partial/zero movement, full output, task errors/cancel, duplicate requests, and restart. Aggregate full results; multiple reads are not an atomic stock snapshot.
