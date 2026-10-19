#!/usr/bin/env python3
"""Test documented mod adapters using cct-run scripted peripherals, not Minecraft."""
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
    parser.add_argument("--cct-run", required=True)
    args = parser.parse_args()
    board = BLOCKS.findall((REFS / "mod-create.md").read_text())[0]
    ap = BLOCKS.findall((REFS / "mod-advanced-peripherals.md").read_text())
    assert board.rstrip().endswith("return render")
    assert ap[0].rstrip().endswith("return reply")
    assert ap[1].rstrip().endswith("return decode")

    def display(size, failed=False):
        return {"type": "scripted", "peripheral_type": "Create_DisplayLink", "methods": {
            "getSize": {"returns": size},
            "clear": {"returns": [], "main_thread": False},
            "setCursorPos": {"returns": [], "main_thread": False},
            "writeBytes": {"returns": [], "main_thread": False},
            "update": {"error": "injected update error"} if failed else {"returns": []},
        }}

    fixture = {
        "files": {"board.lua": board, "reply.lua": ap[0], "decode.lua": ap[1]},
        "peripherals": {
            "left": display([2, 4]),
            "right": display([2, 4], True),
            "front": display([0, 0]),
            "top": {"type": "scripted", "peripheral_type": "chat_box", "methods": {
                "sendMessage": {"sequence": [[None, "CHAT_MESSAGE is on cooldown"], [True], [False, "rejected"]]},
            }},
            "bottom": {"type": "scripted", "peripheral_type": "chat_box", "methods": {
                "sendMessage": {"error": "injected disconnect"},
            }},
            "back": {"type": "scripted", "peripheral_type": "chatBox", "methods": {
                "sendMessageToPlayer": {"returns": [True]},
            }},
        },
        "timeline": [{"tick": 60, "do": "event", "name": "chat",
                      "args": ["example-uuid", "Alice", "??", False,
                               "工厂".encode("utf-8").decode("latin-1")]}],
    }
    program = r'''
local render = require("board")
local reply = require("reply")
local decode = require("decode")
local count = 0
local function check(value)
    assert(value, "mod example check failed: " .. (count + 1))
    count = count + 1
end
local link = peripheral.wrap("left")
local text = "\229\183\165\229\142\130\230\181\139\232\175\149\229\164\154"
local ok, status = render(link, {text, "Inventory"})
check(ok and status == "submitted")
ok, status = render(link, {text, "Inventory"})
check(ok and status == "unchanged")
ok, status = render(link, {text, "Inventory"}, true)
check(ok and status == "submitted")
local bad = peripheral.wrap("right")
ok = render(bad, {"X"})
check(ok == false)
ok = render(bad, {"X"})
check(ok == false)
ok = render(peripheral.wrap("front"), {"X"})
check(ok == false)
local chat = peripheral.wrap("top")
check(peripheral.hasType(chat, "chat_box"))
check(not peripheral.hasType("back", "chat_box"))
ok, status = reply(chat, "Alice", text)
check(ok == false and status:find("cooldown", 1, true))
ok, status = reply(chat, "Alice", text)
check(ok and status == "submitted")
ok, status = reply(chat, "Alice", text)
check(ok == false and status == "rejected")
ok = reply(peripheral.wrap("bottom"), "Alice", text)
check(ok == false)
ok = reply(chat, "", text)
check(ok == false)
local incoming = decode(table.pack(os.pullEvent("chat")))
check(incoming and incoming.uuid == "example-uuid" and incoming.player == "Alice")
check(incoming.text == "\229\183\165\229\142\130" and incoming.hidden == false)
incoming = decode({[1] = "chat", [3] = "[say]", [4] = "hello", [5] = true})
check(incoming and incoming.uuid == nil and incoming.text == "hello" and incoming.hidden)
check(decode({"key", 81}) == nil)
print("mod example checks: " .. count)
'''
    with tempfile.TemporaryDirectory(prefix="cct-mod-examples-") as directory:
        directory = pathlib.Path(directory)
        entry = directory / "checks.lua"
        entry.write_text(program, encoding="utf-8")
        fixture_path = directory / "fixture.json"
        fixture_path.write_text(json.dumps(fixture), encoding="utf-8")
        result = subprocess.run([
            str(pathlib.Path(args.cct_run).resolve()), "run", str(entry),
            "--fixture", str(fixture_path), "--timeout", "6", "--out", str(directory / "runs"),
        ], capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise SystemExit(result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        if summary.get("status") != "ok":
            raise SystemExit(result.stdout)
        records = [json.loads(line) for line in
                   (pathlib.Path(summary["run_dir"]) / "trace.jsonl").read_text().splitlines()]
        calls = [r for r in records if r.get("kind") == "peripheral_call"]
        updates = [r for r in calls if r.get("peripheral") == "right" and r.get("method") == "update"]
        if len(updates) != 2:
            raise SystemExit("failed render incorrectly cached as success")
        sent = [r for r in calls if r.get("peripheral") == "top" and r.get("method") == "sendMessage"]
        if len(sent) != 3 or any(r["args"][1].get("player") != "Alice" or
                                 r["args"][1].get("utf8") is not True for r in sent):
            raise SystemExit("AP options-table protocol mismatch")
        writes = [r for r in calls if r.get("peripheral") == "left" and r.get("method") == "writeBytes"]
        expected = list("工厂测试".encode("utf-8"))
        actual = writes[0]["args"][0] if writes else None
        # Lua tables cross the Java boundary as maps; trace keeps one-based keys.
        if isinstance(actual, dict) and set(actual) == {str(i) for i in range(1, len(expected) + 1)}:
            actual = [actual[str(i)] for i in range(1, len(expected) + 1)]
        if actual != expected:
            raise SystemExit("display did not clip BMP text to four columns as UTF-8 bytes")
        source = json.dumps(records, ensure_ascii=False)
        if "mod example checks: 17" not in source:
            raise SystemExit("missing completed assertion count")
        print("PASS: 17 mod-adapter assertions; trace checks confirm UTF-8 byte table, rows/cols,")
        print("failed-render retry, AP options, nil/false/exception handling and event order.")
        print("Boundary: scripted responses/event injection; no Java mod execution or game validation.")


if __name__ == "__main__":
    main()
