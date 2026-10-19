# Application engineering

[Core](../SKILL.md) · [Recovery](state-and-recovery.md) · [Networking](networking.md)

## Structure by responsibility

Keep the launcher small. Separate configuration, device adapters, pure decision logic, production state, and rendering when the program warrants modules. Do not force a multi-file framework onto a short script.

One owner should perform material actions and ledger updates. Detect optional capabilities instead of comparing version strings alone. On disconnection, invalidate affected wrappers and pause consequential work; reconnect does not prove an interrupted action failed.

## Disposable configuration example

This example normalizes presentation settings and may overwrite them. It is **not** a production-state save protocol. Corrupt orders/intents require [recovery](state-and-recovery.md), never default initialization.

```lua
-- settings_store.lua: disposable presentation settings only.
local PATH = "/data/config.json"
local DEFAULTS = { monitor = nil, volume = 1, refresh = 5, speakers = {} }

local function clamp(x, lo, hi, default)
    x = tonumber(x)
    if not x or x ~= x or x == math.huge or x == -math.huge then return default end
    return math.max(lo, math.min(hi, x))
end

local function normalize(raw)
    raw = type(raw) == "table" and raw or {}
    local cfg = {}
    cfg.monitor = type(raw.monitor) == "string" and raw.monitor ~= "" and raw.monitor or nil
    cfg.volume = clamp(raw.volume, 0, 3, DEFAULTS.volume)
    cfg.refresh = math.floor(clamp(raw.refresh, 1, 3600, DEFAULTS.refresh))
    cfg.speakers = {}
    local seen = {}
    for _, name in ipairs(type(raw.speakers) == "table" and raw.speakers or {}) do
        if type(name) == "string" and not seen[name] then
            seen[name] = true
            cfg.speakers[#cfg.speakers + 1] = name
        end
    end
    return cfg
end

local function load_config()
    if not fs.exists(PATH) then return normalize(nil), nil end
    local opened, h = pcall(fs.open, PATH, "r")
    if not opened or not h then return normalize(nil), "Cannot open config file" end
    local read_ok, text = pcall(h.readAll)
    local close_ok = pcall(h.close)
    if not read_ok or not close_ok then return normalize(nil), "Cannot read/close config file" end
    local raw, err = textutils.unserialiseJSON(text)
    if raw == nil then return normalize(nil), "Config file corrupt, using defaults: " .. tostring(err) end
    return normalize(raw), nil
end

local function save_config(cfg)
    local text = textutils.serialiseJSON(normalize(cfg))
    local prepared, h, err = pcall(function()
        local free = fs.getFreeSpace("/")
        if free ~= "unlimited" and free < #text then return nil, "Not enough disk space" end
        if not fs.exists("/data") then fs.makeDir("/data") end
        return fs.open(PATH, "w")
    end)
    if not prepared then return false, tostring(h) end
    if not h then return false, tostring(err) end
    local written, write_err = pcall(h.write, text)
    local closed, close_err = pcall(h.close)
    if not written then return false, tostring(write_err) end
    if not closed then return false, tostring(close_err) end
    return true
end

local cfg, warning = load_config()
if warning then printError(warning) end
cfg.volume = cfg.volume + 0.5
print(save_config(cfg))
```

The complete file read and schema validation happen before callers use the settings. Defaults are appropriate here because these fields do not authorize replaying production. This direct overwrite can lose settings on interruption; use recoverable generations if those settings require durability.

## Preserve exceptions and business returns

A protected call must preserve nil-bearing tuples and must not relabel a false business result as success. This helper reports exceptions and returns the full pcall tuple. It does not decide the API's success semantics.

```lua
local function safely(action, ...)
    local result = table.pack(pcall(action, ...))
    if not result[1] then
        printError("Action failed: " .. tostring(result[2]))
    end
    return table.unpack(result, 1, result.n)
end
```

For an application object defined with `function App:log(...)`, call `app:log(...)`. This does not change the dot convention of wrapped CC peripherals. Diagnostic logging should not hide the original outcome if logging itself fails; production persistence failures must remain explicit and gate actions.

## Installation and updates

Preserve existing startup and user data. Use data-only manifests with validated paths, lengths, and pinned hashes when distributing updates. Download into staging, validate complete contents, retain a known previous generation, then switch using a documented recovery procedure. Do not delete the working installation before a replacement is verified.

Reject absolute/traversing archive paths and unexpected files. An empty Lua environment does not make a downloaded executable manifest safe. Integrity hashes obtained from the same untrusted source do not authenticate an update; use a trusted release channel or independently trusted signature when needed.

## Logs and resource budgets

Log request IDs, stage, selected device, actual movement, and failure reason. Prefer structured allowlisted fields over dumping entire objects/requests; simple token-redaction patterns do not cover every secret. Rotate logs within a configured size budget and keep enough evidence to reconcile unresolved work.

Bound polling, parallel batches, response sizes, queue depth, and retries. Publish concise summaries of full observations. Follow trace cursors forward and expose retention gaps; repeatedly reading the same earliest slice is not monitoring progress.
