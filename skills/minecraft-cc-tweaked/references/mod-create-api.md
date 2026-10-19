# Create 6.0.10: annotated Lua method declarations

[Guide](mod-create.md) · [Artifact scope](mod-source-baseline.md)

Generated directly from class-file `LuaFunction` annotations without executing the jar.
This is a declaration/name index, **not a Lua argument or return-value specification**.
See the guide and current implementation for contracts. Names alone do not prove device availability, permissions, dependencies, or valid state.

`*` means mainThread=true; an unmarked method is not guaranteed never to yield.
Merge inherited declarations as appropriate, and verify dynamic plugins, owner capabilities, and optional integrations with runtime getMethods.
Java class names locate implementation; they are not peripheral.find type names. Returned-object methods are not necessarily block-peripheral methods.

Artifact SHA-256: `ef87fe5709f1ba1f5b8bb20a2925b5afb4669e178fd6d8bf10c167759eefe37a`.

## PackageLuaObject

Implementation: `com.simibubi.create.compat.computercraft.implementation.luaObjects.PackageLuaObject`. Parent: `java.lang.Object`.

`isEditable`*, `getAddress`*, `setAddress`*, `list`*, `getItemDetail`*, `getOrderData`*.

## PackageOrderLuaObject

Implementation: `com.simibubi.create.compat.computercraft.implementation.luaObjects.PackageOrderLuaObject`. Parent: `java.lang.Object`.

`getOrderID`*, `getIndex`*, `isFinal`*, `getLinkIndex`*, `isFinalLink`*, `list`*, `getItemDetail`*, `getCrafts`*.

## CreativeMotorPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.CreativeMotorPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`setGeneratedSpeed`*, `getGeneratedSpeed`.

## DisplayLinkPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.DisplayLinkPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`setCursorPos`, `getCursorPos`, `getSize`*, `isColor`, `isColour`, `write`, `writeBytes`, `clearLine`, `clear`, `update`*.

## FrogportPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.FrogportPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`setAddress`*, `getAddress`*, `getConfiguration`*, `setConfiguration`*, `list`*, `getItemDetail`*.

## NixieTubePeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.NixieTubePeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`setText`*, `setTextColour`*, `setTextColor`*, `setSignal`*.

## PackagerPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.PackagerPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`makePackage`*, `list`*, `getItemDetail`*, `getAddress`*, `setAddress`*, `getPackage`*.

## PostboxPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.PostboxPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`setAddress`*, `getAddress`*, `list`*, `getItemDetail`*, `getConfiguration`*, `setConfiguration`*.

## RedstoneRequesterPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.RedstoneRequesterPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`request`*, `setRequest`*, `setCraftingRequest`*, `getRequest`*, `getConfiguration`*, `setConfiguration`*, `setAddress`*, `getAddress`*.

## RepackagerPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.RepackagerPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`makePackage`*, `list`*, `getItemDetail`*, `getAddress`*, `setAddress`*, `getPackage`*.

## SequencedGearshiftPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.SequencedGearshiftPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`rotate`*, `move`*, `isRunning`.

## SignalPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.SignalPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`getState`, `isForcedRed`, `setForcedRed`*, `listBlockingTrainNames`, `getSignalType`, `cycleSignalType`*.

## SpeedControllerPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.SpeedControllerPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`setTargetSpeed`*, `getTargetSpeed`.

## SpeedGaugePeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.SpeedGaugePeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`getSpeed`.

## StationPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.StationPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`assemble`*, `disassemble`*, `setAssemblyMode`*, `isInAssemblyMode`, `getStationName`, `setStationName`*, `isTrainPresent`, `isTrainImminent`, `isTrainEnroute`, `getTrainName`, `setTrainName`*, `hasSchedule`, `getSchedule`, `setSchedule`*, `canTrainReach`, `distanceTo`.

## StickerPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.StickerPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`isExtended`, `isAttachedToBlock`, `extend`*, `retract`*, `toggle`*.

## StockTickerPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.StockTickerPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`stock`*, `getStockItemDetail`*, `requestFiltered`*, `list`*, `getItemDetail`*.

## StressGaugePeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.StressGaugePeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`getStress`, `getStressCapacity`.

## TableClothShopPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.TableClothShopPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`isShop`*, `getAddress`*, `setAddress`*, `getPriceTagItem`*, `setPriceTagItem`*, `getPriceTagCount`*, `setPriceTagCount`*, `getWares`*, `setWares`*.

## TrackObserverPeripheral

Implementation: `com.simibubi.create.compat.computercraft.implementation.peripherals.TrackObserverPeripheral`. Parent: `com.simibubi.create.compat.computercraft.implementation.peripherals.SyncedPeripheral`.

`isTrainPassing`, `getPassingTrainName`.
