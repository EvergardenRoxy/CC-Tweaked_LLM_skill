# Events, yielding, and concurrency

[Core](../SKILL.md) · [Design](design-thinking.md) · [Testing](testing.md)

`os.pullEvent(filter)` waits for matching events; other events delivered to that waiting coroutine may be discarded. `sleep` waits for a timer internally. Some device calls yield for main-thread work. A callback that waits can therefore disrupt other input or consume a timer event before the main loop sees it.

Do not assume all peripheral methods yield, or that all terminal-like mod methods are immediate. Use the installed implementation and relevant annotations as evidence. Tick duration and wall-clock response under lag are different quantities.

## Short callbacks: one event loop

```lua
local timer = os.startTimer(1)
while true do
    local event, arg = os.pullEvent()
    if event == "timer" and arg == timer then
        print("tick")
        timer = os.startTimer(1)
    elseif event == "key" and arg == keys.q then
        break
    end
end
```

This example has no yielding work inside its callbacks. Giving a timer an ID does not recover it if another wait consumes its event.

## Responsive input alongside device work

Use a listener that only parses/validates/enqueues input, a worker that owns actuators, and a poller that publishes observations. `parallel` distributes events to eligible child coroutines; each coroutine's filters and yields still matter. Parent queues and mod input buffers are finite.

The following is a small **volatile dashboard demonstration**, not a durable production-order queue. Touch toggles a redstone output; Q stops it. Configure the intended unique inventory/monitor and actual output polarity before use. The listener rejects overload visibly instead of dropping already queued commands. A real order system must persist acceptance when required and return a request-specific rejection.

```lua
-- Volatile dashboard demo: keep yielding reads out of the input listener.
local chest = peripheral.find("inventory") or error("No inventory found", 0)
local mon = peripheral.find("monitor") or error("No monitor attached", 0)
local OUTPUT_SIDE = "back"           -- redstone line that runs the machine

local state = { items = 0, running = false, handled = 0 }
local queue = {}                     -- commands waiting for the worker

local function draw()
    mon.clear()
    mon.setCursorPos(1, 1)
    mon.write(("Items %d"):format(state.items))
    mon.setCursorPos(1, 2)
    mon.write(state.running and "RUNNING" or "STOPPED")
    mon.setCursorPos(1, 3)
    mon.write(("Commands %d"):format(state.handled))
end

-- Poller: peripheral reads may yield.
local function poller()
    while true do
        local n = 0
        for _, item in pairs(chest.list()) do n = n + item.count end
        state.items = n
        draw()
        sleep(1)
    end
end

-- Listener: no yielding device calls; capacity is deliberately bounded.
local function listener()
    while true do
        local ev = { os.pullEvent() }
        if (ev[1] == "monitor_touch" and ev[2] == peripheral.getName(mon))
            or (ev[1] == "key" and ev[2] == keys.q) then
            if #queue < 32 then
                queue[#queue + 1] = ev
                os.queueEvent("work")
            else
                printError("Command rejected: queue full")
            end
        end
    end
end

-- 3. Worker: runs queued commands. It checks the queue before every wait,
--    so a "work" event lost while it was busy does not lose a command.
local function worker()
    while true do
        while #queue > 0 do
            local ev = table.remove(queue, 1)
            if ev[1] == "monitor_touch" then
                state.running = not state.running
            elseif ev[1] == "key" and ev[2] == keys.q then
                state.running = false
            end
            redstone.setOutput(OUTPUT_SIDE, state.running)
            state.handled = state.handled + 1
            draw()
        end
        os.pullEvent("work")
    end
end

parallel.waitForAny(poller, listener, worker)
```

This example leaves the output in its last commanded state on unexpected termination. For consequential machinery, choose the required stop policy, arrange cleanup on normal exits/errors, and use physical interlocks if loss of computer power must stop the plant. Software cleanup cannot run after every shutdown.

## Ownership and overload

- Treat the queue as the source of pending work; wake-up events only notify the worker. Check queued work before waiting again.
- Bound queues and processing batches. Explicitly reject or backpressure new commands; only replace old entries when they are intentionally disposable telemetry.
- A read/decide/write sequence containing a yield can interleave with another coroutine. Assign one owner or revalidate; cooperative scheduling does not eliminate races.
- Do not render from multiple yielding workers without coordination. Core monitor operations and mod display updates have different scheduling contracts.
- Handle peripheral source names and event-specific payloads. AP chat and Create events do not share an argument layout.
- `waitForAny` ends sibling work when one function returns. `waitForAll` waits for every task. Plan shutdown and error propagation explicitly.

For burst tests use unique request IDs, meaningful input cadence, realistic device delays/cooldowns, and separate tests for duplicates and queue capacity. A successful burst is evidence for that load, not a universal no-loss guarantee. See [testing](testing.md).
