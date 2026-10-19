# Create logistics, packages, and trains

[Create](mod-create.md) · [Artifact scope](mod-source-baseline.md) · [Method index](mod-create-api.md)

The contracts describe the reviewed Create 6.0.10 jar. Confirm network links, addresses, block state, methods, and current configuration. An accepted request is not a delivery.

## Packages and ports

| Type | Operations | Boundary |
|---|---|---|
| `Create_Packager` | `makePackage`, `list`, `getItemDetail`, `getAddress`, `setAddress([address])`, `getPackage` | `makePackage` returns whether a package was made, not whether it arrived; `list` reads the attached inventory |
| `Create_Repackager` | Corresponding package methods | Repackages existing packages; inspect its state instead of treating it as a plain packager |
| `Create_Frogport` / `Create_Postbox` | Address/configuration, inventory methods | Contents, binding, and physical transport all matter |

Port configuration values in this artifact are **`send_recieve`** (actual spelling) and `send`. An unbound port can return nil or false. Read the configuration before and after changing it; setting an address does not create a transport route.

`getPackage()` can return nil or a Lua object with `isEditable`, `getAddress`, `setAddress`, `list`, `getItemDetail`, `getOrderData`. It is not a peripheral network name. Modify only editable objects; package objects from events may be read-only snapshots.

Order objects expose `getOrderID`, `getIndex`, `isFinal`, `getLinkIndex`, `isFinalLink`, `list`, `getItemDetail`, `getCrafts`. The final-package and final-link flags do not confirm arrival.

## Stock Ticker

`Create_StockTicker.stock([detailed])` returns network stock summaries; `getStockItemDetail(index)` reads details for an entry of that summary. `list`/`getItemDetail` instead access the **payment inventory**. Never substitute one total for the other.

`requestFiltered(address, filter1, filter2, ...)` broadcasts a request and returns the number of items matched and requested, not delivered. Each filter can use a positive `_requestCount`; omitting a limit may request all matches. The implementation removes `_requestCount` from the passed table, so do not reuse that mutable object as the durable request record.

The filter supports detailed comparisons and `_op`; it is not AP ItemFilter. Summary indexes change between reads; persist item IDs/components and request IDs, never indexes, across restarts. Multiple network reads are not an atomic snapshot.

## Redstone Requester

| Method | Reviewed contract |
|---|---|
| `setRequest(item1, ..., item9)` | Nine positional item/nil arguments, not one outer array; item strings or name/count tables |
| `setCraftingRequest(count, item1, ..., item9)` | Craft count, then nine slots; confirm what the craft count means in the current version |
| `getRequest()` | Configuration, not triggered/completed work |
| `request()` | Void trigger; track delivery separately |
| `get/setConfiguration` | `allow_partial` or `strict` |
| `get/setAddress` | Address configuration, not route validation |

Reject invalid IDs and zero, negative, or unreasonable counts before calling; the jar's own parser limits are not recipe rules. Save the intent to trigger when needed; if it is unclear whether a request went out, check pending work and the destination before repeating it.

## Shops

`Create_TableClothShop.isShop()` checks shop state. The address, price, and wares getters/setters configure a shop; they do not confirm payment. Check the positional arguments of `setWares` instead of guessing an outer array. Change only what the task requires.

## Stations, signals, and observers

`Create_Station` reads assembly mode/name and present/imminent/enroute status. `setAssemblyMode`, `setStationName`, `assemble`, and `disassemble` change the world; never call them just to explore.

Train name and schedule methods need a train at the station; a missing train, track, or schedule can raise an error. `canTrainReach(destinationFilter)` returns boolean/reason; `distanceTo(destinationFilter)` returns distance or nil/reason. The destination is a station-name filter, not coordinates.

Schedule tables are converted from NBT, with snake_case fields and one-based lists. Base a new schedule on one read from the current version. An empty table is not a valid way to clear a schedule.

`Create_Signal` exposes its state, a forced-red getter/setter, the names of blocking trains, and the signal type. Clearing forced red does not prove the route is clear. `Create_TrainObserver` exposes `isTrainPassing`/`getPassingTrainName`; passage is not station arrival or unloading completion.

## Events and settlement

Events put the source peripheral name first. Train events include `train_imminent`, `train_arrival`, `train_departure`; `train_signal_state_change` includes state. Take package and port event names and payloads from the implementation or a real trace; do not guess them.

Track acceptance, creation, dispatch, physical arrival, and final accounting separately. The historical precision-mechanism test did not cover trains or logistics.
