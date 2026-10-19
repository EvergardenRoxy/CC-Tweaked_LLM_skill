# Events, yielding, and concurrency

[Core](../SKILL.md) · [Design](design-thinking.md) · [Testing](testing.md)

`os.pullEvent(filter)` waits for a matching event and discards every other event delivered to that coroutine meanwhile. `sleep` is a timer plus such a filtered wait. Generic inventory/tank/energy methods and most mod methods wait for the server's main thread. A callback that waits can therefore drop user input, or swallow a timer event that the main loop was waiting for.

Not every peripheral method yields (native terminal and monitor drawing returns immediately), and terminal-like mod methods are not necessarily immediate. Check the installed implementation or its `mainThread` annotations. Under server lag, a game tick can take much longer than 0.05 seconds of real time.

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

This works because no callback yields. Comparing timer IDs does not bring back a timer event that another wait already discarded; if it is lost, the loop never wakes again.

## Responsive input alongside device work

Split the program into a **listener** that only parses, validates, and queues input; a **worker** that alone drives actuators; and a **poller** that reads devices and publishes what it sees. `parallel` hands each event to every child coroutine whose current filter matches, so a coroutine waiting on a peripheral call misses events only for itself. The computer's event queue and mod input buffers are still finite.

The following is a small **in-memory dashboard demo**, not a durable order queue. Touching the monitor toggles a redstone output; Q stops it. Before use, make sure only the intended inventory and monitor match, and check the output polarity. When the queue is full, the listener rejects the new command visibly instead of dropping queued ones. A real order system must save accepted orders when needed and send a rejection to the specific requester.

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

-- Worker: runs queued commands. It checks the queue before every wait,
--    so a "work" event missed while it was busy does not lose a command.
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

Both the poller and the worker call `draw`; that is safe here only because monitor drawing does not yield, so one `draw` always finishes before another starts.

This example leaves the output in its last commanded state on unexpected termination. For consequential machinery, choose the required stop policy, arrange cleanup on normal exits/errors, and use physical interlocks if loss of computer power must stop the plant. Software cleanup cannot run after every shutdown.

## Ownership and overload

- The queue is the record of pending work; wake-up events only notify the worker. Check the queue before waiting again.
- Bound queues and processing batches. Reject or slow down new commands explicitly; drop old entries only when they are disposable telemetry where only the newest value matters.
- A read/decide/write sequence containing a yield can interleave with another coroutine. Assign one owner or revalidate; cooperative scheduling does not eliminate races.
- Do not let several workers draw if drawing can yield. Native monitor calls do not yield; mod display updates (for example Create's `update()`) can.
- Check the source peripheral name and the event's own argument layout. AP chat events and Create events are laid out differently.
- `waitForAny` stops all other tasks as soon as one returns; `waitForAll` waits for every task. An error in any task ends the whole `parallel` call. Plan shutdown explicitly.

For burst tests, use unique request IDs, a realistic input rate, realistic device delays and cooldowns, and separate tests for duplicate IDs and a full queue. A passing burst shows the program handled that load, not that it never loses input. See [testing](testing.md).
