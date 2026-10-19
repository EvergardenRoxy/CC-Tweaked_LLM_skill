# Create: motion, stress, and displays

[Artifact scope](mod-source-baseline.md) · [Logistics/trains](mod-create-logistics.md) · [Create with AP](mod-create-ap.md) · [Declaration index](mod-create-api.md)

Contracts below refer to the reviewed Create 6.0.10 artifact. Discover the selected device's actual network name, types, and methods first. Native Create integration, CC generic handlers, and AP extensions are distinct layers. No connection implies invented `startCrafting`, `getProgress`, or `setRecipe` methods.

## Motion contracts

| Type | Methods | Meaning |
|---|---|---|
| `Create_Speedometer` | `getSpeed()` | Signed actual speed; target speed is a different quantity |
| `Create_Stressometer` | `getStress()`, `getStressCapacity()` | Guard zero capacity before ratios |
| `Create_RotationSpeedController` | `getTargetSpeed()`, `setTargetSpeed(integer)` | Void setter; target readback does not prove the plant is moving |
| `Create_CreativeMotor` | `getGeneratedSpeed()`, `setGeneratedSpeed(integer)` | Creative device; not a default survival dependency |
| `Create_SequencedGearshift` | `rotate(amount [, speedModifier])`, `move(...)`, `isRunning()` | New commands clear/replace the current sequence; do not repeatedly reset it |
| `Create_Sticker` | `isExtended()`, `isAttachedToBlock()`, `extend()`, `retract()`, `toggle()` | Actions return booleans; confirm needed physical state |

Rotation-controller limits are delegated to the actual block's scroll behavior/configuration. Do not assume a universal RPM bound. Select the controller driving the intended plant and verify actual speed/stress and material effect within the authorized scope.

Gearshift amount is made absolute in this artifact; the optional modifier has an implementation default. Choose explicit parameters from the current machine behavior. Wait for `isRunning()==false` or a diagnosed failure before the next command. Main-thread methods yield; keep them out of the input listener.

Pausing auxiliary feed, changing a clutch signal, and stopping rotation have different effects. Confirm wiring/polarity and already-held inputs. Shared power can also drive a display or unrelated machine.

## Motion events

Create's synchronized peripheral events prepend the **source attachment name**:

| Event | Payload after event name |
|---|---|
| `speed_change` | source, speed |
| `stress_change` | source, stress, capacity |
| `overstressed` | source |

Filter source, read initial state, and reconcile after reconnection. Events do not replace completion evidence.

## `Create_DisplayLink`

| Method | Reviewed contract |
|---|---|
| `getSize()` | **rows, columns**, unlike core term/monitor; main-thread |
| `setCursorPos(x,y)`, `getCursorPos()` | One-based; upper bounds need application clipping |
| `clear()`, `clearLine()` | Clear buffers; clearing does not reset cursor |
| `write(text)` | Java string conversion; do not assume raw Lua UTF-8 bytes decode correctly |
| `writeBytes(bytes)` | Integer table read in order and masked to bytes, then decoded as UTF-8; string input takes an ASCII path |
| `update()` | Main-thread, void; submits the source update, not proof of visible rendering |
| `isColor()`, `isColour()` | False; no native CC palette-style colors |

Confirm target, starting row, drive/power, and visible result. One instance can maintain multiple lines; the implementation does not require one link per row.

Save the following as `create_board.lua`. It assumes **valid BMP text** with one codepoint per target column, not arbitrary emoji/combining-character width. Failed submissions do not update its cache. Use `force` after target changes/external edits. For malformed or untrusted strings, validate before calling; character clipping itself may raise an encoding error.

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

`submitted` means these calls did not raise an error. Confirm actual target rendering separately. The getSize/update calls can yield, so render in an appropriate worker. Cache identity is the wrapped object plus frame; replace/invalidate on reconnect.

## Nixie tubes

`Create_NixieTube` provides `setText(text [, color])`, `setTextColour`/`setTextColor`, and `setSignal([firstTable [, secondTable]])`. Color and signal schemas are this mod's contracts, not CC color masks or DisplayLink byte tables. Verify supported strings/fields before writing.

For material processing, use the **effective recipe and actual topology**, not a remembered Create recipe. See [production](recipes-and-production.md). Validate actual processing, pause boundaries, overload, destination capacity, and restart windows separately from displays/API calls.
