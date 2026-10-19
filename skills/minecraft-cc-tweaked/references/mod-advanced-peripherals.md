# Advanced Peripherals: discovery, chat, and sensors

[Artifact scope](mod-source-baseline.md) · [Storage](mod-advanced-peripherals-storage.md) · [Extensions](mod-advanced-peripherals-extended.md) · [Create integration](mod-create-ap.md) · [Method index](mod-advanced-peripherals-api.md)

The contracts describe the reviewed AP 1.21.1-0.8.2a jar. The installed game's actual methods and configuration override this page and older notes. Types use snake_case, including `chat_box`, `player_detector`, `geo_scanner`, `inventory_manager`, `me_bridge`, and `rs_bridge`.

The `getName`/`setName` methods that AP peripherals share manage AP's display name, not the wired network name; use `peripheral.getName` for that. `getConfiguration()` shows the device's configuration and operations. AP also adds a global `advancedperipherals` API that reports Minecraft/AP/addon versions and lists player-stat keys, where installed.

## Chat sending

`chat_box.sendMessage(text [, options])` and `sendFormattedMessage(json [, options])` use an **options table**. Options include `player` (name or UUID), `range`, `prefix`, `brackets` (a two-character string), `bracketsColor`, and `utf8`. The older `sendMessageToPlayer`/`sendFormattedMessageToPlayer` methods do not exist in this version.

`utf8=true` makes AP decode the Lua string's bytes as UTF-8, so Chinese text arrives correctly. Formatted JSON can use `\uXXXX` escapes instead. `sendToast(options)`/`sendFormattedToast(options)` require message, title, and player; in the formatted version, title and message are JSON. `narrateMessage` is queued and delayed by its own rules.

A `true` result means the message was dispatched; it can still reach zero players after filtering, and it is not a read receipt. Keep nil/reason, false, and raised errors visible; invalid JSON, invalid brackets, excessive length, and cooldown are different failures.

Save this single-attempt adapter as `ap_reply.lua`. Queueing, limited retries, permission checks, and delivery tracking belong to the application.

```lua
-- ap_reply.lua: this jar uses an options table, not positional player args.
local function reply(chat, player, text)
    if type(player) ~= "string" or player == "" then return false, "Missing player" end
    local called, accepted, reason = pcall(chat.sendMessage, text, { player = player, utf8 = true })
    if not called then return false, tostring(accepted) end
    if accepted ~= true then return false, tostring(reason or "Message not accepted") end
    return true, "submitted"
end
return reply
```

## Cooldown and configuration

Do not assume an earlier test's cooldown or the jar default is the server's value. Read `getConfiguration().operations` and its actual keys. In this version, `chatMessage.getCooldown()` on that returned table gives the remaining milliseconds, and entries also show cost and default values. There is no `getOperationCooldown` peripheral method.

Send from a worker with limited pacing and retries; do not read the configuration on every event. Keep a real, nonzero cooldown when testing throttling and queueing.

## Chat events

The reviewed layout is:

```text
event, uuid, username, message, hidden, messageUtf8
```

The UUID can be nil. Use `messageUtf8` for non-ASCII input; in `message`, characters above U+00FF are already replaced by `?`. Unlike Create events, this event does not start with the peripheral name. A message starting with `$` is hidden from other players and the `$` is removed; hidden does not mean authenticated.

```lua
-- ap_chat_event.lua: decode the uploaded jar's event layout only.
local function decode(ev)
    if ev[1] ~= "chat" or type(ev[3]) ~= "string" then return nil end
    local text = type(ev[6]) == "string" and ev[6] or ev[4]
    if type(text) ~= "string" then return nil end
    return { uuid = ev[2], player = ev[3], text = text, hidden = ev[5] == true }
end
return decode
```

This decoder targets this one AP version; check the actual layout before using it. Limited event buffers and several chat boxes can cause lost or duplicate messages; use request IDs instead of assuming nothing is lost. Never run chat text as Lua.

## Player Detector

| Method family | Contract |
|---|---|
| `getOnlinePlayers()` | All online players, filtered by dimension/spectator settings; not a range query |
| `getPlayersInRange(range)`, `isPlayersInRange(range)` | List, or boolean, of players within range |
| `isPlayerInRange(range, player)` | Range comes first; checks distance per axis (a cube), not a sphere |
| `getPlayersInCoords(a,b)` and boolean variants | Position tables with x/y/z |
| `getPlayersInCubic(x,y,z)` and variants | Relative cubic extents, not arbitrary absolute world points |
| `getPlayer(player [, detailed])` | The Lua name in this version; may return nil or raise; coordinates may include configured inaccuracy |
| `getOwner([detailed])` | For pocket/turtle forms that have an owner; may be nil for the block |
| `getPlayerStat(...)` | Use real stat keys (see `advancedperipherals` API); do not guess old IDs |

`player_join`, `player_leave`, and `player_changed_dimension` carry UUID, username, fromDimension, toDimension (nil where not applicable). `player_death` carries UUID, username, and damage-type ID. Configuration filters apply; joining the server is not entering the detection range.

## Environment and resource sensors

| Type | Method families and boundaries |
|---|---|
| `environment_detector` | Biome, light, time, dimension, moon, weather, entities, sleep; check the returned fields |
| `block_reader` | `getBlockName`, `getBlockState`, `getBlockData`, `hasBlockEntity`; air or blocks without data may return nil; can be disabled in config |
| `geo_scanner` | `scanBlocks(radius)`, `chunkAnalyze([filter])`; fuel, cooldown, and range limits; the old name `scan` is gone |
| `distance_detector` | `getDistance` returns a cached value, `calculateDistance` measures now (main thread); settings for detection, laser, transparency, period, range |
| `energy_detector`, `fluid_detector`, optional `gas_detector` | Transfer rate and limits, not stored amount; units depend on the resource |
| `nbt_storage` | `load`, `save(snbtOrTable)`; may raise parse or size errors or return false/reason; not a safe replacement for files |

Use the jar's names exactly, including the mismatched `getIgnoreTransparent` / `setIgnoreTransparency` and the misspelled `getLastTransferedId`. Transfer detectors also have `getReadyTransferId`. Do not "correct" the spelling, and do not treat a cached reading as a fresh measurement.
