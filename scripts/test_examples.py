#!/usr/bin/env python3
"""Run changed reliability examples in cct-run, without Minecraft/world access."""
import argparse
import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFS = ROOT / "skills/minecraft-cc-tweaked/references"
BLOCKS = re.compile(r"^```lua\n(.*?)^```", re.M | re.S)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cct-run", required=True, help="path to cct-run launcher")
    args = parser.parse_args()
    gate = BLOCKS.findall((REFS / "state-and-recovery.md").read_text())[0]
    engineering = BLOCKS.findall((REFS / "app-engineering.md").read_text())
    logging = next(code for code in engineering if 'local function safely(' in code)
    config = next(code for code in engineering if 'local function save_config(' in code)
    assert gate.rstrip().endswith("return after_persist")
    assert config.count("local cfg, warning = load_config()") == 1
    # Export the same documented helpers; retain their actual bodies unchanged.
    config = config.split("local cfg, warning = load_config()", 1)[0]
    files = {
        "gate.lua": gate,
        "logging.lua": logging + "\nreturn safely\n",
        "config.lua": config + "\nreturn { load = load_config, save = save_config }\n",
    }
    program = r'''
local gate = require("gate")
local safely = require("logging")
local cfg = require("config")
local count = 0
local actions = 0
local function check(value)
    assert(value, "check failed: " .. (count + 1))
    count = count + 1
end
local function action() actions = actions + 1 return 1 end
local result = gate(function() return false, "disk full" end, action)
check(result.stage == "not_persisted" and actions == 0)
result = gate(function() return nil, "cannot open" end, action)
check(result.stage == "not_persisted" and actions == 0)
result = gate(function() error("save failed") end, action)
check(result.stage == "not_persisted" and actions == 0)
result = gate(function() return true end, action)
check(result.stage == "called" and actions == 1 and result.result[2] == 1)
result = gate(function() return true end, function() return false, "cooldown" end)
check(result.stage == "called" and result.result[2] == false and result.result[3] == "cooldown")
result = gate(function() return true end, function() return 0 end)
check(result.result[2] == 0)
result = gate(function() return true end, function() end)
check(result.stage == "called" and result.result.n == 1)
result = gate(function() return true end, function() actions = actions + 1 error("after change") end)
check(result.stage == "uncertain" and actions == 2)
local ok, accepted, reason = safely(function() return false, "cooldown" end)
check(ok == true and accepted == false and reason == "cooldown")
local values = table.pack(safely(function() return nil, "empty", nil end))
check(values.n == 4 and values[1] and values[2] == nil and values[3] == "empty")
ok = safely(function() error("display failed") end)
check(ok == false)
check(cfg.save({ volume = 2, refresh = 3, speakers = {} }) == true)
local restored, warning = cfg.load()
check(restored.volume == 2 and restored.refresh == 3 and warning == nil)
local h = assert(fs.open("/data/config.json", "w")) h.write("broken") h.close()
restored, warning = cfg.load()
check(restored.volume == 1 and warning ~= nil)
-- Fault injection only at the file handle boundary, not a replacement config adapter.
local real_open = fs.open
local closed = false
fs.open = function(path, mode)
    if path == "/data/config.json" and mode == "w" then
        return { write = function() error("injected write error") end,
                 close = function() closed = true end }
    end
    return real_open(path, mode)
end
ok = cfg.save({ volume = 1, refresh = 2, speakers = {} })
fs.open = real_open
check(ok == false and closed)
fs.open = function(path, mode)
    if path == "/data/config.json" and mode == "w" then
        return { write = function() end, close = function() error("injected close error") end }
    end
    return real_open(path, mode)
end
ok = cfg.save({ volume = 1, refresh = 2, speakers = {} })
fs.open = real_open
check(ok == false)
fs.open = function(path, mode)
    if path == "/data/config.json" then error("injected open error") end
    return real_open(path, mode)
end
ok = cfg.save({})
check(ok == false)
restored, warning = cfg.load()
check(restored.volume == 1 and warning ~= nil)
fs.open = real_open
closed = false
fs.open = function(path, mode)
    if path == "/data/config.json" and mode == "r" then
        return { readAll = function() error("injected read error") end,
                 close = function() closed = true end }
    end
    return real_open(path, mode)
end
restored, warning = cfg.load()
fs.open = real_open
check(restored.volume == 1 and warning ~= nil and closed)
fs.open = function(path, mode)
    if path == "/data/config.json" and mode == "r" then
        return { readAll = function() return "{}" end,
                 close = function() error("injected close error") end }
    end
    return real_open(path, mode)
end
restored, warning = cfg.load()
fs.open = real_open
check(restored.volume == 1 and warning ~= nil)
check(cfg.save({ volume = 0/0, refresh = math.huge }) == true)
restored = cfg.load()
check(restored.volume == 1 and restored.refresh == 5)
print("reliability example checks: " .. count)
'''
    with tempfile.TemporaryDirectory(prefix="cct-skill-examples-") as tmp:
        tmp = pathlib.Path(tmp)
        fixture = tmp / "fixture.json"
        fixture.write_text(json.dumps({"files": files}), encoding="utf-8")
        entry = tmp / "checks.lua"
        entry.write_text(program, encoding="utf-8")
        result = subprocess.run(
            [str(pathlib.Path(args.cct_run).resolve()), "run", str(entry),
             "--fixture", str(fixture), "--out", str(tmp / "runs")],
            capture_output=True, text=True, timeout=45,
        )
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        if summary.get("status") != "ok":
            raise SystemExit(result.stdout)
        run_dir = pathlib.Path(summary["run_dir"])
        print("PASS: cct-run status ok; gate, return preservation and config I/O checks")
        trace = run_dir / "trace.jsonl"
        count = re.search(r"reliability example checks: (\d+)", trace.read_text())
        if count is None or int(count[1]) != 22:
            raise SystemExit("missing completed reliability assertion count")
        print("PASS: 22 reliability assertions")

        examples = BLOCKS.findall((REFS / "events-and-concurrency.md").read_text())
        dashboard = next(code for code in examples if 'local function poller()' in code)
        entry.write_text(dashboard, encoding="utf-8")
        fixture.write_text(json.dumps({
            "peripherals": {
                "top": {"type": "inventory", "size": 27},
                "left": {"type": "monitor", "blocks": [3, 2]},
            },
            "timeline": [
                {"tick": 5, "do": "event", "name": "monitor_touch", "args": ["unselected-monitor", 1, 1]},
                {"tick": 6, "do": "event", "name": "monitor_touch", "args": ["left", 1, 1]},
                {"tick": 7, "do": "event", "name": "key", "args": [81, False]},
            ],
        }), encoding="utf-8")
        result = subprocess.run(
            [str(pathlib.Path(args.cct_run).resolve()), "run", str(entry),
             "--fixture", str(fixture), "--timeout", "2", "--out", str(tmp / "runs")],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 2:
            raise SystemExit(result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        if summary.get("status") != "timeout":
            raise SystemExit(result.stdout)
        rows = {}
        trace = pathlib.Path(summary["run_dir"]) / "trace.jsonl"
        for line in trace.read_text().splitlines():
            record = json.loads(line)
            if record.get("kind") == "screen" and record.get("source") == "left":
                rows.update(record.get("lines", {}))
        if rows.get("2", "").strip() != "STOPPED" or rows.get("3", "").strip() != "Commands 2":
            raise SystemExit("dashboard did not handle both touch and key: " + repr(rows))
        print("PASS: documented dashboard handles monitor touch and keyboard stop without a mod")


if __name__ == "__main__":
    main()
