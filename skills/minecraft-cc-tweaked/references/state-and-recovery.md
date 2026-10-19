# Production state and recovery

[Core](../SKILL.md) · [Production](recipes-and-production.md)

## Classify the data

| Data | Read failure policy |
|---|---|
| Disposable display settings | Validate, warn, and use documented defaults if appropriate |
| Accepted orders, request IDs, intents, settlement counts | Preserve evidence; recover a valid generation or pause for reconciliation |
| Observation/render cache | Rebuild; never treat it as the production ledger |

A missing main file does not prove first installation: backups, staging files, existing workpieces, or unsettled outputs may indicate interrupted work. A parseable backup does not establish which world actions occurred.

## Recoverable persistence protocol

Implement only the durability the task needs, but state its boundaries.

1. Validate schema, revision, identities, count ranges, and pending intent. A decoded table can still be invalid.
2. Write a separate staging file. Check opening, writing, and closing; reread and validate it. A free-space estimate cannot replace the actual result.
3. Preserve a valid previous generation before promotion. An existing backup destination can make `fs.copy` fail: define and check backup replacement, rather than swallowing its exception.
4. Define recovery for interruption during each move/copy/promotion stage. Never delete the only valid copy first. Deleting an old directory then moving a new one is not an atomic update.
5. Permit a new external action only after its required intent is saved. After execution, record confirmed effects. If settlement cannot be saved, pause and retain evidence.

Disk files and the game world are separate systems. A higher revision or newer timestamp does not prove that a pending action happened. A recoverable sequence of renames does not guarantee that the main path always exists or that physical storage has synchronized.

## Gate the action on persistence

Save as `after_persist.lua`. The caller must supply a real `save_intent` implementation whose contract is true on success and false/nil or an exception on failure.

```lua
-- after_persist.lua: called is not the same as business success.
local function after_persist(save_intent, action)
    local saved = table.pack(pcall(save_intent))
    if not saved[1] then
        return { stage = "not_persisted", reason = tostring(saved[2]) }
    end
    if saved[2] ~= true then
        return { stage = "not_persisted", reason = tostring(saved[3] or "save rejected") }
    end

    local result = table.pack(pcall(action))
    if not result[1] then
        -- The action may have changed the world before raising an error.
        return { stage = "uncertain", reason = tostring(result[2]) }
    end
    return { stage = "called", result = result }
end

return after_persist
```

`not_persisted` means this call did not execute the action; the caller must not feed through another branch. `uncertain` means the action may already have changed the world; reconcile before retrying. `called` means no exception: the packed tuple contains the pcall flag at index 1 and business values from index 2.

This helper implements neither persistence nor exactly-once execution. Interpret false, nil, zero/partial movement, returned jobs, and void setters using the specific API contract.

## Restart reconciliation

Stop new feed, inspect ledger generations and complete relevant inventories/state, and compare pending intents with actual source, work position, and destination. Account for players and external automation. If completion cannot be determined, expose the ambiguity and pause.

Persist deduplication records if IDs must survive restart; document their retention and expiry behavior. Count actual accepted output rather than nominal yield. Do not equate a byproduct inventory's total item count with failed attempts.

| Fault window | Required result |
|---|---|
| Main corrupted after several saves | Backup actually advances; recovery source and rollback range are visible |
| Main and backup both invalid | Preserve files and pause; no empty-ledger reset |
| Intent open/write/close/promotion fails | No new material action; recoverable generation remains |
| Action executes, settlement fails | Reconcile before repeating the action |
| Final input consumed, result not settled | Inspect workpiece/output/transfer boundaries separately |
| Destination full or partial move | Count only confirmed movement; retain remaining intent |

Run the documented gate tests from the repository; they do not validate every persistence protocol or power-loss window.
