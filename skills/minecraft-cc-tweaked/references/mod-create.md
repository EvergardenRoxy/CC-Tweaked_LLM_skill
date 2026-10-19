# Create: motion, stress, and displays

[Artifact scope](mod-source-baseline.md) · [Logistics/trains](mod-create-logistics.md) · [Create with AP](mod-create-ap.md) · [Declaration index](mod-create-api.md)

The contracts below describe the reviewed Create 6.0.10 jar. First discover the selected device's actual network name, types, and methods. Create's own computer integration, CC:T's generic inventory/fluid handlers, and AP's Create extensions are separate layers. None of them provides `startCrafting`, `getProgress`, or `setRecipe`; do not invent such methods.

## Motion contracts

| Type | Methods | Meaning |
|---|---|---|
| `Create_Speedometer` | `getSpeed()` | Signed actual speed; target speed is a different quantity |
| `Create_Stressometer` | `getStress()`, `getStressCapacity()` | Guard zero capacity before ratios |
| `Create_RotationSpeedController` | `getTargetSpeed()`, `setTargetSpeed(integer)` | Returns nothing; reading the target back does not prove the machines are turning |
| `Create_CreativeMotor` | `getGeneratedSpeed()`, `setGeneratedSpeed(integer)` | Creative device; not a default survival dependency |
| `Create_SequencedGearshift` | `rotate(amount [, speedModifier])`, `move(...)`, `isRunning()` | A new command replaces the running sequence; do not resend it repeatedly |
| `Create_Sticker` | `isExtended()`, `isAttachedToBlock()`, `extend()`, `retract()`, `toggle()` | Actions return booleans; confirm the resulting physical state |

The speed controller's limits come from the block's own scroll setting and configuration; do not assume a fixed RPM range. Select the controller that drives the intended machines, then check the actual speed, stress, and material effect within what the user allowed.

This jar uses the absolute value of `amount`, so a negative amount does not reverse direction; the optional modifier has its own default. Pass explicit parameters chosen from the machine's observed behavior. Wait until `isRunning()` returns false, or a failure is diagnosed, before sending the next command. Main-thread methods yield, so keep them out of the input listener.

Stopping the auxiliary feed, switching a clutch, and stopping rotation have different effects. Confirm wiring and signal polarity, and what the machines already hold. The same rotation source may also drive displays or unrelated machines.

## Motion events

Create's peripheral events put the **source peripheral name** first:

| Event | Payload after event name |
|---|---|
| `speed_change` | source, speed |
| `stress_change` | source, stress, capacity |
| `overstressed` | source |

Filter by source, read the initial state at startup, and re-read after reconnecting. An event is not proof that work completed.

## `Create_DisplayLink`

| Method | Reviewed contract |
|---|---|
| `getSize()` | **rows, columns**, unlike core term/monitor; main-thread |
| `setCursorPos(x,y)`, `getCursorPos()` | One-based; upper bounds need application clipping |
| `clear()`, `clearLine()` | Clear the buffer; the cursor is not reset |
| `write(text)` | Converts through a Java string; UTF-8 text from Lua comes out garbled |
| `writeBytes(bytes)` | Integer table read in order, each value masked to a byte, then decoded as UTF-8; a string argument is treated as ASCII |
| `update()` | Main-thread, returns nothing; sends the update, which does not prove the board shows it |
| `isColor()`, `isColour()` | Always false; no CC palette colors |

Confirm the target, starting row, that the link is powered/driven, and the visible result. One Display Link can fill several lines; you do not need one link per row.

Save the following as `create_board.lua`. It assumes **valid BMP text** with one character per display column; emoji and combining characters will misalign. A failed update does not update its cache. Pass `force` after the target changes or something else wrote to it. Validate malformed or untrusted strings first: `utf8.offset` raises an error on invalid UTF-8.

```lua
-- create_board.lua
local last_link, last_frame
local function render(link, lines, force)
    local sized, rows, cols = pcall(link.getSize)
    if not sized then return false, tostring(rows) end
    if type(rows) ~= "number" or type(cols) ~= "number" or rows < 1 or cols < 1 then
        return false, "No valid display target"
    end
    local visible = {}
    for y = 1, rows do
        local text = lines[y] or ""
        local stop = utf8.offset(text, cols + 1)
        visible[y] = stop and text:sub(1, stop - 1) or text
    end
    local frame = rows .. ":" .. cols .. ":" .. table.concat(visible, "\n")
    if not force and link == last_link and frame == last_frame then return true, "unchanged" end
    local ok, err = pcall(function()
        link.clear()
        for y = 1, rows do
            local bytes = {}
            for i = 1, #visible[y] do bytes[i] = visible[y]:byte(i) end
            link.setCursorPos(1, y)
            link.writeBytes(bytes)
        end
        link.update()
    end)
    if not ok then return false, tostring(err) end
    last_link, last_frame = link, frame
    return true, "submitted"
end
return render
```

`submitted` only means no call raised an error; confirm on the real display. `getSize` and `update` yield, so call `render` from a worker, not the input listener. The cache is keyed by the wrapped object and the frame, so a reconnect (new wrapper) redraws.

## Nixie tubes

`Create_NixieTube` provides `setText(text [, color])`, `setTextColour`/`setTextColor`, and `setSignal([firstTable [, secondTable]])`. Their color names and signal tables are Create's own formats, not CC color masks or Display Link byte tables. Check the supported values before writing.

For processing materials, use the **pack's effective recipe and the actual machine layout**, not a remembered Create recipe; see [production](recipes-and-production.md). Test real processing, pausing, overload, full outputs, and restarts separately from display and API calls.
