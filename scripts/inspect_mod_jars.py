#!/usr/bin/env python3
"""Read class-file LuaFunction annotations without loading Minecraft or executing mods.

Usage: inspect_mod_jars.py --create create.jar --ap AdvancedPeripherals.jar
Outputs audit JSON and the two generated method-name references. Hand-written
guides remain responsible for Lua argument/return contracts and runtime gates.
"""
import argparse
import hashlib
import json
import pathlib
import struct
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
REFS = ROOT / "skills/minecraft-cc-tweaked/references"
EXPECTED_SHA256 = {
    "create": "ef87fe5709f1ba1f5b8bb20a2925b5afb4669e178fd6d8bf10c167759eefe37a",
    "ap": "1bf3e11a1aea4cb4ab024d2fd43261d02565c304a705c6a379e7ebfa4c2d277e",
}


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def take(self, size):
        value = self.data[self.pos:self.pos + size]
        if len(value) != size:
            raise ValueError("truncated class file")
        self.pos += size
        return value

    def u1(self):
        return self.take(1)[0]

    def u2(self):
        return struct.unpack(">H", self.take(2))[0]

    def u4(self):
        return struct.unpack(">I", self.take(4))[0]


def parse_class(data):
    r = Reader(data)
    if r.u4() != 0xCAFEBABE:
        raise ValueError("not a Java class")
    r.u2()
    major = r.u2()
    pool = [None] * r.u2()
    i = 1
    while i < len(pool):
        tag = r.u1()
        if tag == 1:
            # Class/method/annotation identifiers are ASCII; Java string constants
            # may contain modified UTF-8 and are not used as identity evidence here.
            pool[i] = r.take(r.u2()).decode("utf-8", errors="replace")
        elif tag == 3:
            pool[i] = struct.unpack(">i", r.take(4))[0]
        elif tag == 4:
            pool[i] = struct.unpack(">f", r.take(4))[0]
        elif tag in (5, 6):
            r.take(8)
            i += 1
        elif tag in (7, 8, 16, 19, 20):
            pool[i] = r.u2()
        elif tag in (9, 10, 11, 12, 17, 18):
            r.take(4)
        elif tag == 15:
            r.take(3)
        else:
            raise ValueError("unsupported constant-pool tag " + str(tag))
        i += 1

    def annotation(a):
        name = pool[a.u2()]
        values = {}
        for _ in range(a.u2()):
            key = pool[a.u2()]
            values[key] = element(a)
        return {"type": name, "values": values}

    def element(a):
        tag = chr(a.u1())
        if tag in "BCDFIJSZs":
            value = pool[a.u2()]
            return bool(value) if tag == "Z" else value
        if tag == "e":
            return {"enum": pool[a.u2()], "value": pool[a.u2()]}
        if tag == "c":
            return pool[a.u2()]
        if tag == "@":
            return annotation(a)
        if tag == "[":
            return [element(a) for _ in range(a.u2())]
        raise ValueError("unsupported annotation value " + tag)

    def attributes():
        result = {}
        for _ in range(r.u2()):
            name = pool[r.u2()]
            result[name] = r.take(r.u4())
        return result

    r.u2()
    class_name = pool[pool[r.u2()]]
    super_index = r.u2()
    superclass = pool[pool[super_index]] if super_index else None
    for _ in range(r.u2()):
        r.u2()
    for _ in range(r.u2()):
        r.take(6)
        attributes()
    methods = []
    for _ in range(r.u2()):
        access = r.u2()
        name, descriptor = pool[r.u2()], pool[r.u2()]
        attrs = attributes()
        for attr_name in ("RuntimeVisibleAnnotations", "RuntimeInvisibleAnnotations"):
            if attr_name not in attrs:
                continue
            a = Reader(attrs[attr_name])
            for _ in range(a.u2()):
                ann = annotation(a)
                if ann["type"] != "Ldan200/computercraft/api/lua/LuaFunction;":
                    continue
                values = ann["values"]
                methods.append({
                    "java_method": name,
                    "descriptor": descriptor,
                    "lua_names": values.get("value") or [name],
                    "main_thread": bool(values.get("mainThread", False)),
                    "public": bool(access & 1),
                    "annotations": values,
                })
    return {"class": class_name.replace("/", "."),
            "superclass": superclass.replace("/", ".") if superclass else None,
            "class_major": major, "methods": methods}


def inspect(path, mod):
    result = {"filename": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "classes": []}
    if result["sha256"] != EXPECTED_SHA256[mod]:
        raise ValueError(mod + " jar differs from this reviewed baseline; review the new binary before regenerating")
    prefix = ("com/simibubi/create/compat/computercraft/" if mod == "create"
              else "de/srendi/advancedperipherals/")
    with zipfile.ZipFile(path) as jar:
        result["metadata"] = jar.read("META-INF/neoforge.mods.toml").decode()
        for name in sorted(jar.namelist()):
            if not name.startswith(prefix) or not name.endswith(".class"):
                continue
            data = jar.read(name)
            cls = parse_class(data)
            if cls["methods"]:
                cls["entry"] = name
                cls["sha256"] = hashlib.sha256(data).hexdigest()
                result["classes"].append(cls)
    return result


def reference(mod, result):
    label = "Create 6.0.10" if mod == "create" else "Advanced Peripherals 0.8.2a"
    entry = "mod-create.md" if mod == "create" else "mod-advanced-peripherals.md"
    lines = ["# " + label + ": annotated Lua method declarations", "",
             "[Guide](" + entry + ") · [Artifact scope](mod-source-baseline.md)", "",
             "Generated from the `LuaFunction` annotations in the jar's class files, without running the jar.",
             "It lists method names only; it **does not describe Lua arguments or return values**.",
             "See the guide and the installed implementation for how to call them. A name here does not prove the device exists in a game, or the needed permissions, dependencies, or state.", "",
             "`*` marks main-thread methods, which yield until the next game tick; unmarked methods may still yield.",
             "A class also has its parent classes' methods. Check plugins, device-form differences, and optional integrations with `peripheral.getMethods` in the game.",
             "Java class names show where the code lives; they are not `peripheral.find` types. Methods of returned objects are not methods of the block peripheral.", "",
             "Artifact SHA-256: `" + result["sha256"] + "`.", ""]
    for cls in result["classes"]:
        lines.extend(["## " + cls["class"].split(".")[-1], "",
                      "Implementation: `" + cls["class"] + "`. Parent: `" + str(cls["superclass"]) + "`.", "",
                      ", ".join("`" + name + "`" + ("*" if method["main_thread"] else "")
                                for method in cls["methods"] for name in method["lua_names"]) + ".", ""])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--create", type=pathlib.Path, required=True)
    parser.add_argument("--ap", type=pathlib.Path, required=True)
    args = parser.parse_args()
    data = {mod: inspect(getattr(args, mod), mod) for mod in ("create", "ap")}
    audit = ROOT / "docs/mod-evidence/1.21.1"
    audit.mkdir(parents=True, exist_ok=True)
    (audit / "api-index.json").write_text(json.dumps({"schema": "cct-skill/mod-api@1", "mods": data},
                                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for mod, name in (("create", "mod-create-api.md"), ("ap", "mod-advanced-peripherals-api.md")):
        (REFS / name).write_text(reference(mod, data[mod]), encoding="utf-8")
        print(mod, len(data[mod]["classes"]), "annotated classes,",
              sum(len(c["methods"]) for c in data[mod]["classes"]), "method declarations")


if __name__ == "__main__":
    main()
