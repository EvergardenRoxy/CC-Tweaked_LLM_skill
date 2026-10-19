# Advanced Peripherals 0.8.2a: annotated Lua method declarations

[Guide](mod-advanced-peripherals.md) · [Artifact scope](mod-source-baseline.md)

Generated from the `LuaFunction` annotations in the jar's class files, without running the jar.
It lists method names only; it **does not describe Lua arguments or return values**.
See the guide and the installed implementation for how to call them. A name here does not prove the device exists in a game, or the needed permissions, dependencies, or state.

`*` marks main-thread methods, which yield until the next game tick; unmarked methods may still yield.
A class also has its parent classes' methods. Check plugins, device-form differences, and optional integrations with `peripheral.getMethods` in the game.
Java class names show where the code lives; they are not `peripheral.find` types. Methods of returned objects are not methods of the block peripheral.

Artifact SHA-256: `1bf3e11a1aea4cb4ab024d2fd43261d02565c304a705c6a379e7ebfa4c2d277e`.

## AECraftJob

Implementation: `de.srendi.advancedperipherals.common.addons.ae2.AECraftJob`. Parent: `de.srendi.advancedperipherals.common.util.inventory.BasicCraftJob`.

`getCraftingCPU`, `getUsedBytes`.

## BeaconIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.integrations.BeaconIntegration`. Parent: `java.lang.Object`.

`getLevel`*, `getPrimaryEffect`*, `getSecondaryEffect`*.

## NoteBlockIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.integrations.NoteBlockIntegration`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BlockIntegrationPeripheral`.

`changeNote`*, `changeNoteBy`*, `getNote`*, `playNote`*.

## APLuaAPI

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.luaapi.APLuaAPI`. Parent: `java.lang.Object`.

`getAddonVersions`, `getMCVersion`, `getAPVersion`, `iterPlayerStatKeys`.

## FuelAbility

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.owner.FuelAbility`. Parent: `java.lang.Object`.

`getFuelLevel`*, `getMaxFuelLevel`*, `getFuelConsumptionRate`*, `setFuelConsumptionRate`*.

## AbstractStorageSystemPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.AbstractStorageSystemPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`isConnected`*, `isOnline`*, `getItem`*, `getFluid`*, `getChemical`*, `getItems`*, `getFluids`*, `getChemicals`*, `getCraftableItems`*, `getCraftableFluids`*, `getCraftableChemicals`*, `getCells`*, `getDrives`*, `importItem`*, `exportItem`*, `importFluid`*, `exportFluid`*, `importChemical`*, `exportChemical`*, `getStoredEnergy`*, `getEnergyCapacity`*, `getEnergyUsage`*, `getAverageEnergyInput`*, `getMaxExternalItemStorage`*, `getMaxExternalItemCount`*, `getMaxExternalFluidStorage`*, `getMaxExternalChemicalStorage`*, `getMaxItemStorage`*, `getMaxFluidStorage`*, `getMaxChemicalStorage`*, `getUsedExternalItemStorage`*, `getUsedExternalItemCount`*, `getUsedExternalFluidStorage`*, `getUsedExternalChemicalStorage`*, `getUsedItemStorage`*, `getUsedFluidStorage`*, `getUsedChemicalStorage`*, `getAvailableExternalItemStorage`*, `getAvailableExternalItemCount`*, `getAvailableExternalFluidStorage`*, `getAvailableExternalChemicalStorage`*, `getAvailableItemStorage`*, `getAvailableFluidStorage`*, `getAvailableChemicalStorage`*, `getCraftingTasks`*, `getCraftingTask`*, `cancelCraftingTasks`*, `craftItem`*, `craftFluid`*, `craftChemical`*, `isCraftable`*, `isCrafting`*, `getPatterns`*.

## BaseDetectorPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.BaseDetectorPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getMaxTransferRate`, `getTransferRateLimit`, `setTransferRateLimit`, `getTransferRate`, `getLastTransferedId`, `getReadyTransferId`.

## BlockReaderPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.BlockReaderPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getBlockName`*, `getBlockState`*, `getBlockData`*, `hasBlockEntity`*.

## ChatBoxPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.ChatBoxPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`sendMessage`*, `sendFormattedMessage`*, `sendToast`*, `sendFormattedToast`*, `narrateMessage`*.

## ChunkyPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.ChunkyPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getRadius`.

## ColonyPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.ColonyPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`isInColony`*, `isWithin`*, `amountOfConstructionSites`*, `getColonyID`*, `getColonyName`*, `getColonyStyle`*, `isActive`*, `getLocation`*, `getHappiness`*, `isUnderAttack`*, `isUnderRaid`*, `getCitizenCount`*, `getCitizenLimit`*, `getGraveCount`*, `getCitizens`*, `getCitizen`*, `getVisitors`*, `getBuildings`*, `getWorkOrders`*, `getResearches`*, `getWorkOrderResources`*, `getBuilderResources`*, `getRequests`*.

## CompassPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.CompassPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getFacing`*.

## DistanceDetectorPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.DistanceDetectorPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getLaserVisibility`, `setLaserVisibility`, `getIgnoreTransparent`, `setIgnoreTransparency`, `detectingEntities`, `detectingBlocks`, `getDetectionMode`, `setDetectionMode`, `getDistance`, `calculateDistance`*, `getCalculatePeriodically`, `setCalculatePeriodically`, `getMaxRange`, `setMaxRange`.

## EnvironmentDetectorPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.EnvironmentDetectorPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getBiome`*, `getBlockLightLevel`*, `getSkyLightLevel`*, `getDayLightLevel`*, `getTime`*, `isSlimeChunk`*, `getDimension`*, `listDimensions`*, `getMoon`*, `isRaining`*, `isThunder`*, `isSunny`*, `scanEntities`*, `canSleepHere`*, `canPlayerSleep`*.

## GeoScannerPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.GeoScannerPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`scanBlocks`*, `chunkAnalyze`*.

## InventoryManagerPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.InventoryManagerPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getOwner`, `size`*, `list`*, `importItem`*, `exportItem`*, `wrapStorageItem`*, `isWearing`*, `getEmptySlots`*, `getFreeSlot`*, `getHandSlot`*, `getItemInHand`*, `getItemInOffHand`*.

## MEBridgePeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.MEBridgePeripheral`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.AbstractStorageSystemPeripheral`.

`getMountPaths`, `getCraftingCPUs`*.

## NBTStoragePeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.NBTStoragePeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`load`*, `save`*.

## PlayerDetectorPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.PlayerDetectorPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getOnlinePlayers`*, `getPlayersInCoords`*, `getPlayersInCubic`*, `getPlayersInRange`*, `isPlayersInCoords`*, `isPlayersInCubic`*, `isPlayersInRange`*, `isPlayerInCoords`*, `isPlayerInCubic`*, `isPlayerInRange`*, `getPlayer`*, `getOwner`*, `getPlayerStat`*.

## RSBridgePeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.RSBridgePeripheral`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.AbstractStorageSystemPeripheral`.

`getCrafters`*.

## SaddlePeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.SaddlePeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`capture`*, `release`*, `hasRider`, `getRider`*.

## SmartRailPeripheral

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.SmartRailPeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`hasCarts`, `getCarts`*, `getState`, `setState`, `isActivating`, `setActivating`.

## AutomataBlockHandPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataBlockHandPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`digBlock`*, `useOnBlock`*, `updateBlock`*, `placeBlock`*.

## AutomataChargingPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataChargingPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`chargeTurtle`*.

## AutomataEntityHandPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataEntityHandPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`useOnAnimal`*, `inspectAnimal`*, `searchAnimals`*.

## AutomataEntityTransferPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataEntityTransferPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`captureAnimal`*, `releaseAnimal`*, `getCapturedAnimal`*.

## AutomataItemSuckPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataItemSuckPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`scanItems`*, `collectSpecificItem`*, `collectItems`*.

## AutomataLookPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataLookPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`lookAtBlock`*, `lookAtEntity`*.

## AutomataSoulFeedingPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataSoulFeedingPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`feedSoul`*.

## AutomataWarpingPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataWarpingPlugin`. Parent: `de.srendi.advancedperipherals.common.addons.computercraft.peripheral.plugins.AutomataCorePlugin`.

`savePoint`*, `deletePoint`*, `listPoints`*, `warpToPoint`*, `estimateWarpCost`*, `distanceToPoint`*, `preparePortalWarp`, `activePortalWarp`*.

## BasinIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.create.BasinIntegration`. Parent: `java.lang.Object`.

`inputTanks`*, `outputTanks`*.

## BlazeBurnerIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.create.BlazeBurnerIntegration`. Parent: `java.lang.Object`.

`info`*.

## FilteringBehaviourIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.create.FilteringBehaviourIntegration`. Parent: `java.lang.Object`.

`getFilter`*, `setFilter`*.

## FluidTankIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.create.FluidTankIntegration`. Parent: `java.lang.Object`.

`info`*.

## ScrollValueBehaviourIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.create.ScrollValueBehaviourIntegration`. Parent: `java.lang.Object`.

`getScrollValue`*, `setScrollValue`*.

## InventoryManagerCuriosPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.curios.InventoryManagerCuriosPlugin`. Parent: `java.lang.Object`.

`getCuriosSizes`*, `listCurios`*, `importCuriosItem`*, `exportCuriosItem`*, `wrapCuriosStorageItem`*.

## DimChestIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.dimstorage.DimChestIntegration`. Parent: `java.lang.Object`.

`getOwnerUUID`*, `getOwner`*, `hasOwner`*, `getChannel`*, `setChannel`*.

## EnvironmentRadiationPlugin

Implementation: `de.srendi.advancedperipherals.common.addons.mekanism.EnvironmentRadiationPlugin`. Parent: `java.lang.Object`.

`getRadiation`*, `getRadiationRaw`*.

## EnderCellIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.powah.EnderCellIntegration`. Parent: `java.lang.Object`.

`getStoredEnergy`*, `getMaxEnergy`*, `getChannel`, `setChannel`*, `getMaxChannels`.

## EnergyCellIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.powah.EnergyCellIntegration`. Parent: `java.lang.Object`.

`getStoredEnergy`*, `getMaxEnergy`*.

## FurnatorIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.powah.FurnatorIntegration`. Parent: `java.lang.Object`.

`isBurning`, `getStoredEnergy`*, `getMaxEnergy`*, `getCarbon`*, `getFuelSlot`*.

## MagmatorIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.powah.MagmatorIntegration`. Parent: `java.lang.Object`.

`getStoredEnergy`*, `getMaxEnergy`*, `isBurning`, `getFuelTank`.

## ReactorIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.powah.ReactorIntegration`. Parent: `java.lang.Object`.

`isRunning`*, `getFuel`*, `getCarbon`*, `getRedstone`*, `getStoredEnergy`*, `getMaxEnergy`*, `getTemperature`*, `getUraniniteSlot`*, `getRedstoneSlot`*, `getCarbonSlot`*.

## SolarPanelIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.powah.SolarPanelIntegration`. Parent: `java.lang.Object`.

`getStoredEnergy`*, `getMaxEnergy`*, `canSeeSky`.

## ThermoIntegration

Implementation: `de.srendi.advancedperipherals.common.addons.powah.ThermoIntegration`. Parent: `java.lang.Object`.

`getStoredEnergy`*, `getMaxEnergy`*, `getCoolantTank`.

## SmartGlassesAPI

Implementation: `de.srendi.advancedperipherals.common.smartglasses.SmartGlassesAPI`. Parent: `java.lang.Object`.

`isEquipped`*, `getOwner`*, `pingSmartChest`*, `smartChestList`*, `smartChestImportItem`*, `smartChestExportItem`*, `smartHandPos`*, `smartHandMove`*, `smartHandDropItem`*, `smartHandSuckItem`*, `smartHandAttack`*, `smartHandDig`*, `smartHandUse`*.

## ModulePeripheral

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.ModulePeripheral`. Parent: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`.

`getModules`, `hasModule`, `getModule`.

## KeyboardFunctions

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.keyboard.KeyboardFunctions`. Parent: `java.lang.Object`.

`isCapturingKeys`, `isCapturingMouse`, `setCaptureMouse`, `isHandlingInteraction`, `setHandlingInteraction`.

## NightVisionFunctions

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.nightvision.NightVisionFunctions`. Parent: `java.lang.Object`.

`isNightVisionEnabled`, `enableNightVision`.

## OverlayGlassesFunctions

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.OverlayGlassesFunctions`. Parent: `java.lang.Object`.

`createObject`, `createBlock`, `createBox`, `createSphere`, `createTexture`, `createTorus`, `createTriangle`, `createCircle`, `createItem`, `createLine`, `createRectangle`, `createText`, `getObject`, `removeObject`, `clear`, `getObjectsCount`, `getGuiSize`, `getEyePosition`, `update`, `isAutoUpdating`, `setAutoUpdate`.

## OverlayObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.OverlayObject`. Parent: `java.lang.Object`.

`getType`, `getId`.

## BlockObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.BlockObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.BoxObject`.

`getBlock`, `setBlock`, `getStates`, `setStates`.

## BoxObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.BoxObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.ThreeDimensionalObject`.

`getSizes`, `setSizes`.

## ItemObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.ItemObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.RenderableObject`.

`getItem`, `setItem`.

## LineObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.LineObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.RenderableObject`.

`getEndPos`, `setEndPos`.

## RectangleObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.RectangleObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.RenderableObject`.

`getSizes`, `setSizes`.

## RenderableObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.RenderableObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.OverlayObject`.

`getPos`, `setPos`.

## TextureObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.TextureObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.ThreeDimensionalObject`.

`getSizes`, `setSizes`, `getWidth`, `getHeight`, `getImageSize`, `setWidth`, `setHeight`, `setImageSize`, `getPixel`, `setPixel`, `getAllPixels`, `getPixels`, `setPixels`, `load`.

## TriangleObject

Implementation: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.TriangleObject`. Parent: `de.srendi.advancedperipherals.common.smartglasses.modules.overlay.objects.ThreeDimensionalObject`.

`getPos1`, `setPos1`, `getPos2`, `setPos2`, `getPos3`, `setPos3`.

## BasicCraftJob

Implementation: `de.srendi.advancedperipherals.common.util.inventory.BasicCraftJob`. Parent: `java.lang.Object`.

`getId`, `isDone`, `isCanceled`, `isCraftingStarted`, `isCalculationStarted`, `isCalculationNotSuccessful`, `hasErrorOccurred`, `getDebugMessage`, `getRequestedItem`, `getElapsedTime`, `getTotalItems`, `getItemProgress`, `getEmittedItems`, `getUsedItems`, `getMissingItems`, `hasMultiplePaths`, `getFinalOutput`, `cancel`.

## PlayerStorageItemWrapper

Implementation: `de.srendi.advancedperipherals.common.util.inventory.PlayerStorageItemWrapper`. Parent: `java.lang.Object`.

`isValid`*, `isItemStorage`, `isFluidStorage`, `size`*, `list`*, `importItem`*, `exportItem`*, `tanks`*, `importFluid`*, `exportFluid`*.

## BasePeripheral

Implementation: `de.srendi.advancedperipherals.lib.peripherals.BasePeripheral`. Parent: `java.lang.Object`.

`getName`, `setName`*, `getConfiguration`.
