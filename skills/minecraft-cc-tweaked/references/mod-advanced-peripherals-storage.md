# AP inventory, storage bridges, and crafting

[AP](mod-advanced-peripherals.md) · [Artifact scope](mod-source-baseline.md) · [Index](mod-advanced-peripherals-api.md) · [Recovery](state-and-recovery.md)

## Select the layer

For ordinary chest-to-chest transfers, CC:T's own `inventory` methods are usually enough. `inventory_manager` reaches a bound player's inventory; `me_bridge`/`rs_bridge` reach AE2 or Refined Storage networks; Create logistics use a different request model. Their directions, filters, and meaning of success all differ.

Having Create and AP does not mean AE2, Refined Storage, or Mekanism are installed. Check installation, that the bridge is connected and online (`isConnected`, `isOnline`), permissions, and supported resource types. A disconnected network means unknown stock, not zero stock.

## AP ItemFilter

| Field | Reviewed meaning |
|---|---|
| `name` | Item ID, or `#tag` where supported |
| `count` | Maximum amount; always pass a positive integer |
| `fromSlot`, `toSlot` | Slot numbers starting at 1; not directions |
| `components` | Data components as a table or SNBT (1.21 style), not old NBT |
| `matcher` | How components are compared; check the supported values |
| `nbtHash` | A hash of the item's components in this version; not compatible with old NBT hashes |

An empty filter can match everything, so always set `name` and `count`. Unknown items may return nil/reason; malformed fields may raise an error. AP's ItemFilter, Create's filter, and the Stock Ticker filter are three different formats.

## Inventory Manager

`getOwner()` returns **uuid and name as two values**, or nothing when no player is bound. Check the memory card, the owner, and that the player is reachable. `list` is sparse; use the dedicated methods for hand, offhand, armor, and free slots.

`importItem(fromName [, filter])` moves items from a container into the player; `exportItem(toName [, filter])` moves them out. Check the counts actually moved. Some methods accept names like `@front`, meaning a side of the **AP block** itself; this is not valid for CC:T's `pushItems`, pocket devices, or every AP method.

`wrapStorageItem(slot)` returns an object for a storage item in that slot (such as a backpack). Check `isValid` and `isItemStorage`/`isFluidStorage` before using its list/tanks/import/export methods. Discard it when the item moves; it is not a network peripheral.

## Bridge method families

Bridges also have the type `storage_bridge`. Check the exact methods in the [index](mod-advanced-peripherals-api.md):

| Need | Reviewed family |
|---|---|
| Single resource | `getItem`, `getFluid`, `getChemical` |
| Lists | `getItems`, `getFluids`, `getChemicals` |
| Craftable resources | `getCraftableItems/Fluids/Chemicals`, `isCraftable` |
| Movement | `importItem`/`exportItem` and fluid/chemical counterparts |
| Network information | `getCells`, `getDrives`, `getStoredEnergy`, `getEnergyCapacity`, `getEnergyUsage`, `getAverageEnergyInput` |
| Capacity | Max/Used/Available storage and the External variants |
| Tasks | `craftItem`, corresponding resource methods, `getCraftingTasks`, `getCraftingTask`, `cancelCraftingTasks`, `isCrafting` |
| Patterns | `getPatterns` with input/output filters |

Old names such as `listItems` and the old energy methods no longer exist. Chemical methods without Mekanism raise errors; that is not zero stock. The ME bridge's optional CPU-name argument does not exist on RS methods.

## Asynchronous work

A successful `craftItem` returns a job object, not a product count. The job has methods for its ID, done/canceled/calculating/crafting/error state, debug message, requested item, elapsed time, item counts (total, progress, emitted, used, missing), final output, and `cancel`; take the exact names from the index. They belong to the job, not the bridge.

Save the request and job ID when needed. Calculating, queued, crafting, done, and product actually available or delivered are different states. After a restart, find old jobs and check stock before requesting again. Canceling can leave intermediate items behind. ME's `getCraftingCPUs` and RS's `getCrafters` are different methods.

Test missing patterns or materials, offline networks, invalid filters, partial or zero transfers, full outputs, job errors and cancellation, duplicate requests, and restart. Use complete results; several reads are not one consistent stock snapshot.
