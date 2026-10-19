# Create logistics, packages, and trains

[Create](mod-create.md) · [Artifact scope](mod-source-baseline.md) · [Method index](mod-create-api.md)

Contracts refer to the reviewed Create 6.0.10 artifact. Confirm network links, addresses, block state, methods, and current configuration. Request acceptance is not delivery.

## Packages and ports

| Type | Operations | Boundary |
|---|---|---|
| `Create_Packager` | `makePackage`, `list`, `getItemDetail`, `getAddress`, `setAddress([address])`, `getPackage` | Boolean package creation is not receipt; list is the target inventory |
| `Create_Repackager` | Corresponding package methods | Repackaging semantics differ; inspect state rather than treating it as a plain packager |
| `Create_Frogport` / `Create_Postbox` | Address/configuration, inventory methods | Local contents, binding and physical transport matter |

Port configuration values in this artifact are **`send_recieve`** (actual spelling) and `send`. An unbound target can yield nil/false. Read before/after changing configuration; setting an address does not create a transport route.

`getPackage()` can return nil or a Lua object with `isEditable`, `getAddress`, `setAddress`, `list`, `getItemDetail`, `getOrderData`. It is not a peripheral network name. Modify only editable objects; event objects may be read-only snapshots.

Order objects expose `getOrderID`, `getIndex`, `isFinal`, `getLinkIndex`, `isFinalLink`, `list`, `getItemDetail`, `getCrafts`. Final-package/link flags are not destination receipt confirmations.

## Stock Ticker

`Create_StockTicker.stock([detailed])` returns network stock summaries; `getStockItemDetail(index)` reads detail for that summary context. `list`/`getItemDetail` instead access the **payment inventory**. Never substitute one total for the other.

`requestFiltered(address, filter1, filter2, ...)` broadcasts requests and returns the matched/requested item count, not delivered count. Each filter can use a positive `_requestCount`; omitting a limit may request all matches. The implementation removes `_requestCount` from the passed table, so do not reuse that mutable object as the durable request record.

The filter supports detailed comparisons and `_op`; it is not AP ItemFilter. Summary indexes are transient; persist item identity/components and request IDs, not cross-restart indexes. Multiple network reads are not an atomic snapshot.

## Redstone Requester

| Method | Reviewed contract |
|---|---|
| `setRequest(item1, ..., item9)` | Nine positional item/nil arguments, not one outer array; item strings or name/count tables |
| `setCraftingRequest(count, item1, ..., item9)` | Craft count then nine slots; confirm current crafting meaning |
| `getRequest()` | Configuration, not triggered/completed work |
| `request()` | Void trigger; track delivery separately |
| `get/setConfiguration` | `allow_partial` or `strict` |
| `get/setAddress` | Address configuration, not route validation |

Reject invalid IDs and nonpositive/unreasonable counts before calling; the artifact also has parser limits that are not a universal modpack recipe constraint. Persist trigger intent when needed; after uncertainty, check old work and destination before repeating a request.

## Shops

`Create_TableClothShop.isShop()` checks shop state. Address, price-tag item/count, and wares getters/setters configure a shop; they do not confirm payment. Verify `setWares` positional argument schema rather than guessing an outer array. Apply changes only within the user's task.

## Stations, signals, and observers

`Create_Station` reads assembly mode/name and present/imminent/enroute status. `setAssemblyMode`, `setStationName`, `assemble`, and `disassemble` change the world and are not harmless discovery calls.

Train name and schedule methods require an appropriate train/station state; missing trains/tracks/schedules can raise errors. `canTrainReach(destinationFilter)` returns boolean/reason; `distanceTo(destinationFilter)` returns distance or nil/reason. The destination is a station-name filter, not coordinates.

Schedule tables come from NBT conversion with snake_case fields and one-based lists. Read a valid current schema or verify the target version before submitting a copy. An empty table is not a valid universal reset schedule.

`Create_Signal` exposes state, forced-red getter/setter, blocking train names, and signal type/cycling. Removing forced red does not prove the route is clear. `Create_TrainObserver` exposes `isTrainPassing`/`getPassingTrainName`; passage is not station arrival or unloading completion.

## Events and settlement

Synchronized events prepend source attachment name. Train events include `train_imminent`, `train_arrival`, `train_departure`; `train_signal_state_change` includes state. Verify package/port state event strings and payloads from the actual implementation/trace rather than guessing English names.

Track acceptance, creation, dispatch, physical receipt, and final accounting separately. The historical precision-mechanism test did not validate all train/logistics integrations.
