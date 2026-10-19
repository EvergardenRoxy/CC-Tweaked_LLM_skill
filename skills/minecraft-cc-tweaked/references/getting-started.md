# Getting started and startup integration

[Core](../SKILL.md) · [API guide](api-reference.md) · [Testing](testing.md)

For a beginner, first find out which step they are stuck on (where to type, how to read the docs, how to edit files), then give code.

## Three places to type

| Place | Looks like | Accepts | Example |
|---|---|---|---|
| CraftOS shell | `>` prompt | **Program names** and arguments | `ls`, `edit mine.lua`, `mine 10`, `go forward 3`, `refuel all` |
| Lua interpreter | `lua>` after running `lua` | Single Lua statements, run immediately with results shown | `turtle.forward()`, `peripheral.getNames()` |
| Program file | Editor opened by `edit name.lua` | A whole program; save, exit, then run its name from the shell | `edit tunnel.lua`, then `tunnel` |

- Typing `turtle.forward()` at the shell prints `No such program`: the shell treats it as a program name. Run `lua` first, or put the call in a file. The interpreter is the quickest way to try a single function. Leave it with `exit()`.
- Pasting a whole program at the shell prompt does not install it. Save it with `edit`, or download it with `wget`/`pastebin get` where the server allows HTTP.
- In `edit`, press Ctrl to open the menu, then choose Save and Exit.
- Built-in programs cover many tasks: `go`, `turn`, `excavate`, `tunnel`, `refuel`, `equip`, `label`, `peripherals`. `help` shows help topics and `programs` lists every program.
- Hold Ctrl+T to terminate the running program and Ctrl+R to reboot. Neither runs transactional cleanup.

## Reading function signatures

Take `turtle.getItemDetail([slot [, detailed]])`:

- Parentheses are required to call a function: `turtle.forward()` runs it, `turtle.forward` is just the function value.
- Square brackets mark optional arguments and are not typed: `turtle.getItemDetail()`, `turtle.getItemDetail(3)`, and `turtle.getItemDetail(3, true)` are all valid. `[limit=64]` means optional with default 64.
- The Returns section lists each return value separately. Most turtle actions return `success, reason`. A value can be nil, a table, a reason string, or an object; check the specific contract.
- Names are case-sensitive: `turtle.forward()`, not `Turtle.Forward()`.

Use the in-game `help`, the installed ROM, and the [official documentation](https://tweaked.cc/). Older ComputerCraft tutorials and machine translations often contain functions that do not exist (such as `textutils.sha256`) or outdated environment assumptions; check every function before reusing such code.

## Editing with an external editor

1. Run `id` on the computer (or turtle) to get its ID.
2. Its files live in the world save: `saves/<world>/computercraft/computer/<ID>/` in single player, `<world>/computercraft/computer/<ID>/` on a dedicated server. Floppy disks are under `computercraft/disk/<ID>/`. Launchers may place the game directory elsewhere.
3. Edit the files there and save; no world reload is needed. A program that is already running does not reload: stop it and run it again.
4. Without access to the server files, use `wget`/`pastebin get` or a remote-editing tool. Confirm the tool and destination before replacing files.

## Startup integration

Start a program manually and confirm it works before making it start automatically. Keep any existing entry point and application files intact.

In the CC:T 1.120.2 ROM, root `startup`/`startup.lua` and every file in a `startup/` directory are collected and run **one after another**. A long-running earlier entry prevents later ones from starting. When `shell.allow_disk_startup` is enabled and a disk with a startup file is attached, the disk's set runs instead of the computer's own. Adding a file under `/startup/` is therefore not a general way to run beside an existing launcher: inspect the installed ROM and settings, and integrate with the user's current entry point or supervisor.

Keep a manual recovery route: how to terminate the program, disable its launcher, or boot from a disk with an empty `startup.lua` if a broken startup file prevents normal use.

## Common beginner errors

| Symptom | Cause | Fix |
|---|---|---|
| `No such program` for `turtle.forward()` | The shell only runs programs | Run `lua` first, or write a file |
| `No such program` for your file | Wrong directory or misspelled name | Check with `ls`; give the path |
| Turtle function returns `false` and nothing moves | No fuel, or a blocked path | `refuel all`, check `turtle.getFuelLevel()`, read the returned reason |
| Edited file still behaves like the old version | The old program is still running | Stop it with Ctrl+T and run it again |
| `attempt to call nil` | Misspelled name, wrong case, or API missing on this device | Check the docs; a normal computer has no `turtle` API |
| Program should run at boot | No startup entry | Integrate it into `startup.lua` (for example `shell.run("program")`) without removing existing entries |

For non-Latin text, see [text and encoding](text-and-encoding.md). For running programs outside Minecraft, see [testing](testing.md).
