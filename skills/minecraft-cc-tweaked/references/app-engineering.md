# Application engineering

[Core](../SKILL.md) · [Recovery](state-and-recovery.md) · [Networking](networking.md)

## Structure by responsibility

Write large programs only when the user needs that scale (long-running, networked, with a UI). Keep the launcher small. When modules are warranted, separate configuration, device adapters, pure decision logic, production state, and rendering, and load them with `require`. Do not force a multi-file framework onto a short script.

One component should perform world actions and ledger updates. Detect optional features directly instead of comparing version strings. When a device disconnects, discard its wrapper and pause work that depends on it; reconnecting does not prove an interrupted action failed.

## Disposable configuration example

This example cleans up display settings and may overwrite them. It is **not** a way to save production state: corrupt orders or intents need [recovery](state-and-recovery.md), never a reset to defaults.

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

The whole file is read and validated before callers use the settings. Defaults are acceptable here because these fields cannot cause production to be repeated. Overwriting the file directly can lose settings if interrupted; use the recoverable save in [recovery](state-and-recovery.md) if they must survive.

## Preserve exceptions and business returns

A protected call must keep every return value, including nils, and must not turn a `false` result into success. This helper reports errors and returns the full pcall result; deciding what counts as success stays with the caller.

```lua
local function safely(action, ...)
    local result = table.pack(pcall(action, ...))
    if not result[1] then
        printError("Action failed: " .. tostring(result[2]))
    end
    return table.unpack(result, 1, result.n)
end
```

For your own object defined with `function App:log(...)`, call `app:log(...)`; wrapped CC peripherals still use dots. If logging itself fails, it must not hide the original result. Failures to save production state must stay visible and stop new actions.

## Installation and updates

Keep existing startup files and user data. For updates, use a data-only manifest (not Lua code) listing validated paths, sizes, and pinned hashes. Download into a temporary directory, verify everything, keep the previous version, then switch over with a documented recovery procedure. Do not delete the working installation before the replacement is verified.

Reject absolute paths, `..` paths, and unexpected files. Running a downloaded Lua manifest in an empty environment does not make it safe. Hashes downloaded from the same untrusted place do not authenticate an update; use a trusted release source or an independently trusted signature when that matters.

## Logs and resource budgets

Log request IDs, stage, device, actual amounts moved, and failure reasons. Log a fixed set of fields instead of whole objects or requests; simple redaction patterns miss secrets. Rotate logs within a size limit (disk space is small), but keep enough to reconcile unfinished work.

Limit polling rates, parallel batch sizes, response sizes, queue depth, and retries. Summarize complete observations rather than partial ones.
