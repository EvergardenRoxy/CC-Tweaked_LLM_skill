#!/usr/bin/env python3
"""Validate the CC: Tweaked skill.

1. Compiles every ```lua code block in skills/**/*.md with `luac -p` from
   Lua 5.2 (CC: Tweaked runs on Cobalt, a Lua 5.2 runtime), so Lua 5.3+ only
   syntax such as `//`, `&`, `|`, `<<` is rejected.
   Blocks showing wrong code on purpose must use ```text instead.
2. Checks every `<api>.<name>` used in those blocks against the members
   documented on https://tweaked.cc (module, peripheral and generic peripheral
   pages), and flags `<api>:<name>` calls on global APIs.
3. Reads the `luac -l` listing of each block: assigning a global is an error
   (programs must use `local`), and reading a global must name a standard Lua
   or CC: Tweaked global (catches typos such as `pirnt` or `textutil`).
4. Checks that string literals in those blocks are ASCII only: CC terminals
   and monitors cannot display Chinese (or other non-ASCII) text, so example
   messages for print/error/printError must be English. Comments may use
   any language.
5. Checks SKILL.md structure: front matter, line budget, and that every
   `references/*.md` it mentions exists.

Requirements: Python 3.8+, Lua 5.2 compiler (`luac5.2` or `luac` 5.2;
e.g. `apt install lua5.2`), network access on first run.
Downloads are cached in .cache/ (git-ignored).

Usage:
    python3 scripts/validate_skill.py [--luac <path>] [--offline]
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "tweaked.cc"
SKILLS = ROOT / "skills"
SITE = "https://tweaked.cc/"
MAX_SKILL_LINES = 500

BLOCK_RE = re.compile(r"^```lua\n(.*?)^```", re.S | re.M)
PAGE_RE = re.compile(r'href="((?:module|peripheral|generic_peripheral)/[\w.]+\.html)"')
MEMBER_RE = re.compile(r'name="v:([\w.]+)"')

# Global APIs whose members are checked. Values are the doc pages that define them.
CHECKED_APIS = {
    "colors": ["module/colors"], "colours": ["module/colors", "module/colours"],
    "disk": ["module/disk"], "fs": ["module/fs"], "gps": ["module/gps"],
    "help": ["module/help"], "http": ["module/http"], "io": ["module/io"],
    "multishell": ["module/multishell"], "os": ["module/os"],
    "paintutils": ["module/paintutils"], "parallel": ["module/parallel"],
    "peripheral": ["module/peripheral"], "pocket": ["module/pocket"],
    "rednet": ["module/rednet"], "redstone": ["module/redstone"], "rs": ["module/redstone"],
    "settings": ["module/settings"], "shell": ["module/shell"], "term": ["module/term"],
    "textutils": ["module/textutils"], "turtle": ["module/turtle"],
    "vector": ["module/vector"], "window": ["module/window"],
}
# Globals that do not exist in CC: Tweaked although they exist in standard Lua.
MISSING_GLOBALS = {"collectgarbage"}
# Globals a program may read besides the module pages listed on tweaked.cc.
STD_GLOBALS = {
    "_G", "_VERSION", "assert", "error", "getmetatable", "ipairs", "load", "loadfile",
    "dofile", "next", "pairs", "pcall", "print", "rawequal", "rawget", "rawlen", "rawset",
    "require", "select", "setmetatable", "tonumber", "tostring", "type", "xpcall",
    "string", "table", "math", "coroutine", "bit32", "utf8", "debug", "package",
    # CraftOS globals from bios.lua (documented on the _G page)
    "sleep", "write", "printError", "read", "_HOST", "_CC_DEFAULT_SETTINGS",
    # APIs that only exist on some devices or under the shell
    "commands", "turtle", "pocket", "shell", "multishell", "rs",
}
GLOBAL_ACCESS_RE = re.compile(r"\b(GETTABUP|SETTABUP)\b.*;\s*_ENV \"(\w+)\"")


def fetch(path):
    dest = CACHE / path
    if not dest.exists():
        print(f"downloading {SITE}{path}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(SITE + path, headers={"User-Agent": "cct-skill-validator/1.0"})
        with urllib.request.urlopen(req) as resp:
            dest.write_bytes(resp.read())
    return dest.read_text(encoding="utf-8")


def load_api(offline):
    if offline and not (CACHE / "index.html").exists():
        sys.exit("--offline given but .cache/tweaked.cc is empty; run once with network access")
    pages = sorted(set(PAGE_RE.findall(fetch("index.html"))))
    members = {p[: -len(".html")]: set(MEMBER_RE.findall(fetch(p))) for p in pages}
    api = {"__modules__": {p.split("/", 1)[1].lstrip("_") for p in members if p.startswith("module/")}}
    for name, sources in CHECKED_APIS.items():
        missing = [s for s in sources if s not in members]
        if missing:
            sys.exit(f"tweaked.cc no longer has {missing}; update CHECKED_APIS")
        api[name] = set().union(*(members[s] for s in sources))
    return api


def strip_strings_and_comments(src, strings=None):
    """Blank out Lua string literals and comments, keeping line structure.

    If `strings` is a list, (offset, literal) is appended for each string literal.
    """
    out, i, n = [], 0, len(src)
    long_open = re.compile(r"\[(=*)\[")
    while i < n:
        c = src[i]
        if src.startswith("--", i):
            m = long_open.match(src, i + 2)
            if m:
                end = src.find("]" + m.group(1) + "]", m.end())
                end = n if end < 0 else end + len(m.group(1)) + 2
            else:
                end = src.find("\n", i)
                end = n if end < 0 else end
            out.append(re.sub(r"[^\n]", " ", src[i:end]))
            i = end
        elif c in "\"'":
            j = i + 1
            while j < n and src[j] != c and src[j] != "\n":
                j += 2 if src[j] == "\\" else 1
            if strings is not None:
                strings.append((i, src[i:j + 1]))
            out.append('""' + " " * max(0, j - i - 1))
            i = j + 1
        elif long_open.match(src, i):
            m = long_open.match(src, i)
            end = src.find("]" + m.group(1) + "]", m.end())
            end = n if end < 0 else end + len(m.group(1)) + 2
            if strings is not None:
                strings.append((i, src[i:end]))
            out.append('""' + re.sub(r"[^\n]", " ", src[i + 2:end]))
            i = end
        else:
            out.append(c)
            i += 1
    return "".join(out)


def check_api_usage(code, api):
    errors = []
    code = strip_strings_and_comments(code)
    locals_ = set(re.findall(r"\blocal\s+(?:function\s+)?([A-Za-z_]\w*)", code))
    for m in re.finditer(r"(?<![\w.:])([A-Za-z_]\w*)\s*([.:])\s*([A-Za-z_]\w*)", code):
        mod, sep, member = m.groups()
        if mod not in api or mod in locals_:
            continue
        line = code[: m.start()].count("\n") + 1
        if sep == ":":
            errors.append(f"line {line}: {mod}:{member} - CC APIs are called with '.', not ':'")
        elif member not in api[mod]:
            errors.append(f"line {line}: {mod}.{member} is not documented on tweaked.cc")
    for g in MISSING_GLOBALS:
        for m in re.finditer(rf"(?<![\w.:]){g}\s*\(", code):
            errors.append(f"line {code[: m.start()].count(chr(10)) + 1}: {g} does not exist in CC: Tweaked")
    return errors


def check_ascii_strings(code):
    strings = []
    strip_strings_and_comments(code, strings)
    return [f"line {code[:pos].count(chr(10)) + 1}: non-ASCII string {lit} - CC cannot display it, use English"
            for pos, lit in strings if not lit.isascii()]


def check_globals(luac, src_file, api):
    """Use the bytecode listing to find global reads and writes."""
    res = subprocess.run([luac, "-p", "-l", "-l", str(src_file)], capture_output=True, text=True)
    allowed = STD_GLOBALS | api["__modules__"]
    errors = []
    for line in res.stdout.splitlines():
        m = GLOBAL_ACCESS_RE.search(line)
        if not m:
            continue
        op, name = m.groups()
        where = re.search(r"\[(\d+)\]", line)
        at = f"line {where.group(1)}" if where else "?"
        if op == "SETTABUP":
            errors.append(f"{at}: assigns global '{name}' - declare it with local")
        elif name not in allowed:
            errors.append(f"{at}: reads unknown global '{name}' (typo or missing local?)")
    return sorted(set(errors), key=lambda e: int(re.match(r"line (\d+)", e).group(1)) if e[0] == "l" else 0)


def find_luac(explicit):
    candidates = [explicit] if explicit else ["luac5.2", "luac"]
    for c in candidates:
        path = shutil.which(c) if c else None
        if path:
            ver = subprocess.run([path, "-v"], capture_output=True, text=True)
            if "Lua 5.2" in (ver.stdout + ver.stderr):
                return path
            print(f"skipping {path}: not Lua 5.2 ({(ver.stdout + ver.stderr).strip()})")
    sys.exit("missing dependency: a Lua 5.2 compiler (luac5.2), e.g. `apt install lua5.2`")


def check_code_blocks(luac, api):
    failures, total = 0, 0
    with tempfile.TemporaryDirectory() as tmp:
        src_file = pathlib.Path(tmp) / "block.lua"
        for md in sorted(SKILLS.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            for m in BLOCK_RE.finditer(text):
                body = m.group(1)
                if body.strip() == "...":  # placeholder inside the answer-format template
                    continue
                total += 1
                start = text[: m.start()].count("\n") + 2  # first code line in the .md file
                src_file.write_text(body, encoding="utf-8")
                res = subprocess.run([luac, "-p", str(src_file)], capture_output=True, text=True)
                errors = []
                if res.returncode != 0:
                    errors.append(res.stderr.strip().replace(str(src_file), "block"))
                else:
                    errors += check_globals(luac, src_file, api)
                errors += check_api_usage(body, api)
                errors += check_ascii_strings(body)
                if errors:
                    failures += 1
                    print(f"FAIL {md.relative_to(ROOT)}:{start}: {errors[:5]}")
    print(f"lua code blocks: {total} checked, {failures} failed")
    return failures == 0


def check_structure():
    ok = True
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        rel = skill_md.relative_to(ROOT)
        text = skill_md.read_text(encoding="utf-8")
        fm = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not fm or not re.search(r"^name: \S", fm.group(1), re.M) or not re.search(r"^description: \S", fm.group(1), re.M):
            print(f"FAIL {rel}: front matter must contain name and description")
            ok = False
        elif re.search(r"^name: (.+)$", fm.group(1), re.M).group(1).strip() != skill_md.parent.name:
            print(f"FAIL {rel}: front matter name must equal folder name '{skill_md.parent.name}'")
            ok = False
        lines = text.count("\n")
        if lines > MAX_SKILL_LINES:
            print(f"FAIL {rel}: {lines} lines > {MAX_SKILL_LINES}; move details into references/")
            ok = False
        refs = set(re.findall(r"references/[\w.-]+\.md", text))
        refs |= {f"references/{n}" for n in re.findall(r"`([\w-]+\.md)`", text)}
        for ref in sorted(refs):
            if not (skill_md.parent / ref).exists():
                print(f"FAIL {rel}: mentions missing file {ref}")
                ok = False
        for f in sorted((skill_md.parent / "references").glob("*.md")):
            if f"references/{f.name}" not in refs:
                print(f"WARN {rel}: {f.relative_to(ROOT)} is never referenced, the model will not find it")
        print(f"structure: {rel} {lines} lines, {len(refs)} reference files")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--luac", help="path to a Lua 5.2 luac")
    ap.add_argument("--offline", action="store_true", help="only use the cached tweaked.cc pages")
    args = ap.parse_args()
    luac = find_luac(args.luac)
    api = load_api(args.offline)
    ok = check_structure() & check_code_blocks(luac, api)
    print("OK" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
