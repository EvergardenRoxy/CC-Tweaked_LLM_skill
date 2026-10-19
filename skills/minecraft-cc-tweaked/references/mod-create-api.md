# Create 6.0.10: annotated Lua method declarations

[Guide](mod-create.md) · [Artifact scope](mod-source-baseline.md)

Generated from the `LuaFunction` annotations in the jar's class files, without running the jar.
It lists method names only; it **does not describe Lua arguments or return values**.
See the guide and the installed implementation for how to call them. A name here does not prove the device exists in a game, or the needed permissions, dependencies, or state.

`*` marks main-thread methods, which yield until the next game tick; unmarked methods may still yield.
A class also has its parent classes' methods. Check plugins, device-form differences, and optional integrations with `peripheral.getMethods` in the game.
Java class names show where the code lives; they are not `peripheral.find` types. Methods of returned objects are not methods of the block peripheral.

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
