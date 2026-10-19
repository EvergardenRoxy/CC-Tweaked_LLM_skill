# Advanced Peripherals: discovery, chat, and sensors

[Artifact scope](mod-source-baseline.md) · [Storage](mod-advanced-peripherals-storage.md) · [Extensions](mod-advanced-peripherals-extended.md) · [Create integration](mod-create-ap.md) · [Method index](mod-advanced-peripherals-api.md)

Contracts refer to the reviewed AP 1.21.1-0.8.2a binary. Actual methods/configuration win over a matching label or old notes. Types use snake_case, including `chat_box`, `player_detector`, `geo_scanner`, `inventory_manager`, `me_bridge`, and `rs_bridge`.

Common `getName`/`setName` manage AP display names, not wired network names. Use `peripheral.getName` for network identity. Common `getConfiguration()` exposes device/operation configuration. The injected `advancedperipherals` API can report Minecraft/AP/addon versions and iterate player-stat keys; availability still depends on the installation.

## Chat sending

`chat_box.sendMessage(text [, options])` and `sendFormattedMessage(json [, options])` use an **options table**. Options include `player` (name/UUID), range, prefix, brackets (a two-character string), bracketsColor, and utf8. Old `sendMessageToPlayer`/`sendFormattedMessageToPlayer` methods are absent from this reviewed class.

`utf8=true` activates the artifact's byte-string-to-UTF-8 decoding path. Formatted JSON can alternatively use Unicode escapes. `sendToast(options)`/`sendFormattedToast(options)` require message, title, and player; formatted title/message are JSON. `narrateMessage` has its own queued behavior/delay contract.

A true send result means the dispatch call was accepted. Recipient filtering can produce zero recipients while returning true. It is not a read/delivery receipt. Nil/reason, false, and thrown errors must remain visible; invalid JSON/brackets/length and cooldown are distinct failures.

Save this single-attempt adapter as `ap_reply.lua`. Queueing, bounded retry, authorization, and receipt tracking belong to the application.

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

Do not assume the previous test's cooldown or any artifact default is the server's current value. Where exposed, inspect `getConfiguration().operations` and the actual operation keys. In this artifact `chatMessage.getCooldown()` returns remaining milliseconds; configuration entries also expose cost/default metadata. This is a returned object's function, not an invented `getOperationCooldown` peripheral method.

Send in a worker with bounded pacing/retry; do not poll configuration on every listener event. Keep a meaningful nonzero cooldown in tests of throttling/queueing.

## Chat events

The reviewed layout is:

```text
event, uuid, username, message, hidden, messageUtf8
```

UUID can be nil. Prefer messageUtf8 for preserved UTF-8 input; ordinary message may already have lost characters in conversion. This event does not prepend a Create-style peripheral source. `$` hides a message and is removed by the mod; hidden does not mean authenticated.

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

This decoder intentionally targets one verified profile. Select/verify the actual layout before installing it. Finite mod/event buffers and multiple chat sources can produce loss/duplicates; use request IDs and defined retention, not a blanket lossless claim. Never execute chat text as Lua.

## Player Detector

| Method family | Contract |
|---|---|
| `getOnlinePlayers()` | Filtered by dimension/spectator configuration; not a radius query |
| `getPlayersInRange(range)`, `isPlayersInRange(range)` | List or boolean for configured visibility |
| `isPlayerInRange(range, player)` | Range first; reviewed check uses axis distances, not Euclidean-sphere geometry |
| `getPlayersInCoords(a,b)` and boolean variants | Position tables with x/y/z |
| `getPlayersInCubic(x,y,z)` and variants | Relative cubic extents, not arbitrary absolute world points |
| `getPlayer(player [, detailed])` | Actual Lua alias; nil/error possible, coordinates may have configured error |
| `getOwner([detailed])` | Owner-capable pocket/turtle contexts; may be nil for a block |
| `getPlayerStat(...)` | Use actual stat keys/parameters; do not guess legacy IDs |

`player_join`, `player_leave`, `player_changed_dimension` carry UUID, username, fromDimension, toDimension, with nils as appropriate. `player_death` carries UUID, username, damage-type ID. Configuration/range filters apply; joining a server is not entering the detection radius.

## Environment and resource sensors

| Type | Method families and boundaries |
|---|---|
| `environment_detector` | Biome, light, time, dimension, moon, weather, entities, sleep; verify detailed schemas and tuples |
| `block_reader` | `getBlockName`, `getBlockState`, `getBlockData`, `hasBlockEntity`; air/no block entity may produce nil, device can be disabled |
| `geo_scanner` | `scanBlocks(radius)`, `chunkAnalyze([filter])`; fuel/cooldown/range limits; not the old `scan` name |
| `distance_detector` | Cached `getDistance` versus main-thread `calculateDistance`; detection/laser/transparency/period/range settings |
| `energy_detector`, `fluid_detector`, optional `gas_detector` | Transfer rate/limit/max, not stored quantity; resource-specific units |
| `nbt_storage` | `load`, `save(snbtOrTable)`; parse/size errors and false/reason possible; not atomic filesystem persistence |

Preserve the artifact's asymmetric `getIgnoreTransparent` / `setIgnoreTransparency` and misspelled `getLastTransferedId` names. Transfer detectors also expose `getReadyTransferId`. Do not silently normalize API spelling or treat a stale cached reading as a fresh measurement.
