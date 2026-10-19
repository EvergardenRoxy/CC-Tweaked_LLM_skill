# Networking and external I/O

[Core](../SKILL.md) · [Events](events-and-concurrency.md) · [Security](security.md)

## Rednet and modems

Find and open the actual modem: `peripheral.find("modem", rednet.open)`. Wired peripheral names and rednet computer IDs (`os.getComputerID()`) are different things. Wireless range depends on modem type, height, and configuration; ender modems cross dimensions; both ends must be chunk-loaded. Test the real route.

Rednet sends Lua values (tables are serialized) with an optional protocol name. It does not authenticate the sender or guarantee delivery. Use a small message format with a version, request ID, operation, and bounded fields, and reject anything malformed or unsupported. Where important commands may be retried, use acknowledgments and deduplicate by request ID. "Message received" is not "action completed".

`rednet_message` carries sender ID, message, protocol. A raw `modem_message` carries modem side, channel, reply channel, message, and distance (nil across dimensions). Do not mix up the two layouts. Protocol names, channels, sender IDs, and hidden chat prefixes are not authentication.

`rednet.receive` discards other events while it waits. For a UI that also communicates, handle `rednet_message` in the main event loop or run receiving in its own `parallel` task. Never run incoming text as Lua.

## GPS

`gps.locate([timeout [, debug]])` returns `x, y, z` or nil. It needs at least four GPS hosts in range that are not all in one plane (`gps host x y z`), in the same dimension. It gives position only, not facing or a safe path. To find a turtle's facing, locate, move one block, and locate again, but only where that move is safe and allowed.

## HTTP

The server can disable HTTP or restrict hosts, ports, sizes, redirects, and concurrent requests; local and LAN addresses are blocked by default. Use HTTPS, check the status code and content, and always close response handles, including the error response that `http.get` returns as its third value on HTTP errors.

For simple clients, call `http.get`/`http.post` from a worker task. For asynchronous `http.request`, match `http_success`/`http_failure` events to requests by URL in a request table, together with your own timeout timers. Requests to the same URL cannot be told apart, so send them one at a time. Adding fragments or query parameters to tell them apart can change server behavior and is not a general fix.

Limit retries and set timeouts. A client timeout does not prove the server did nothing. Retry reads automatically only when that is safe; before retrying a write that matters, use an idempotency key or check the server state. A local timeout does not cancel the request: handle late responses and close their handles.

For large responses, cap the size you accept, decode carefully, and yield during long processing in a worker so the listener stays responsive. No fixed chunk size guarantees responsiveness everywhere.

## WebSockets and audio

Give each socket one owner and route its `websocket_message`/`websocket_closed` events by URL. Handle closing and failure with a limited, delayed reconnect, not an endless tight loop. Keep tokens out of logs.

For streamed audio, decode DFPWM with `cc.audio.dfpwm` (1.100+). When `speaker.playAudio` returns false, wait for that speaker's `speaker_audio_empty` event and retry the same buffer. Test stopping, disconnecting, and closing the response or socket.
