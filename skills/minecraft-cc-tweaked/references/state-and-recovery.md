# Production state and recovery

[Core](../SKILL.md) · [Production](recipes-and-production.md)

## Classify the data

| Data | Read failure policy |
|---|---|
| Disposable display settings | Validate, warn, and fall back to defaults |
| Accepted orders, request IDs, intents, settled counts | Keep the files; recover from a valid earlier save or pause for reconciliation |
| Observation or render cache | Rebuild it; never treat it as the production ledger |

A missing main file does not prove a first run: backups, temporary files, half-processed items, or unsettled outputs may show interrupted work. A readable backup does not tell you which world actions happened after it was written.

## Recoverable persistence protocol

Build only the durability the task needs, and state what it does not cover.

1. Validate the format, revision, IDs, count ranges, and pending intent. A table that decodes can still be invalid.
2. Write a separate temporary file. Check that opening, writing, and closing succeeded, then read it back and validate it. Checking free space first does not replace checking the write.
3. Keep a valid previous save before replacing the main file. `fs.copy` and `fs.move` fail when the destination exists: delete or rotate the old backup explicitly and check each step instead of swallowing the error.
4. Decide how to recover if the computer stops during each copy, move, or replace step. Never delete the only valid copy first. Deleting the old directory and then moving the new one in is not atomic.
5. Allow a world action only after its intent is saved. Afterwards, record the confirmed effect. If that record cannot be saved, pause and keep the evidence.

Files and the game world are separate systems. A higher revision or newer timestamp does not prove a pending action happened. Even a recoverable sequence of renames does not guarantee that the main file always exists or that the data reached the server's disk.

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

`not_persisted` means the action did not run; the caller must not perform it through another path. `uncertain` means the action may already have changed the world; reconcile before retrying. `called` means no error was raised: `result[1]` is the pcall flag and the action's own return values start at `result[2]`.

This helper provides neither persistence nor exactly-once execution. Interpret false, nil, zero or partial transfers, returned job objects, and setters that return nothing according to each API's contract.

## Restart reconciliation

Stop feeding new material. Read the saved ledger versions and the complete relevant inventories and machine state, and compare pending intents with the actual source, machine, and destination. Allow for players and other automation. If you cannot tell whether an action completed, show that and pause.

Persist deduplication records if request IDs must survive a restart, and document how long they are kept. Count actual delivered output, not expected yield. The number of items in a byproduct chest is not the number of failed attempts.

| Fault window | Required result |
|---|---|
| Main file corrupted after several saves | The backup is current; the recovery source and how much was rolled back are shown |
| Main and backup both invalid | Keep the files and pause; never reset to an empty ledger |
| Saving the intent fails (open, write, close, or replace) | No new world action; a recoverable save remains |
| Action runs, recording the result fails | Reconcile before repeating the action |
| Last input consumed, result not recorded | Check the machine, output, and transfer separately |
| Destination full or partial move | Count only confirmed movement; keep the rest pending |

The repository's tests exercise this helper; they do not validate every save protocol or power-loss moment.
