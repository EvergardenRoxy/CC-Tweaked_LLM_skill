# Networking and external I/O

[Core](../SKILL.md) · [Events](events-and-concurrency.md) · [Security](security.md)

## Rednet and modems

Discover and open the actual modem. Wired device names and rednet computer IDs are different identifiers. Wireless range, dimensions, and chunk loading depend on equipment/configuration; test the intended route.

Rednet provides messages and optional protocol names, not authenticated identity or guaranteed delivery. Use a small data schema with version, request ID, operation, and bounded fields. Reject malformed/unsupported messages. Track acknowledgments and deduplication where consequential commands may be retried. A delivery acknowledgment differs from action completion.

`rednet_message` carries sender ID, message, protocol. A raw `modem_message` includes receiving side, channel, reply channel, message, and distance when available. Do not confuse the two event layouts. Protocol names, channels, sender IDs, and hidden chat prefixes are not authentication.

`rednet.receive` waits and can discard unrelated events in its coroutine. For UI plus communication, dispatch events in a non-yielding listener or use separate tasks. Never evaluate incoming text as Lua.

## GPS

`gps.locate(timeout, debug)` can return coordinates or fail. It requires suitable reachable hosts and geometry. It does not establish facing or a safe path. Record the relevant dimension and frame; do not move destructively just to infer orientation without scope and a recovery plan.

## HTTP

Server rules can disable requests or restrict hosts, ports, sizes, redirects, and concurrency. Use HTTPS when supported, validate status and content, and always close response handles, including failure responses supplied by the API.

Choose synchronous calls in a worker for simple clients. For asynchronous requests, dispatch `http_success`/`http_failure` and owned timer events through a request registry using the actual event identifier. If identical URLs cannot be correlated by the installed API, serialize them or use a server-supported identifier. Appending arbitrary fragments/query strings can change cache/signature/server semantics and is not a universal correlation solution.

Bound retries and timeouts. A client timeout does not prove a server failed to perform an operation. Automatically retry reads only when semantics allow; use an idempotency key or reconcile before retrying a consequential write. A local watchdog may not cancel a pending transport operation; handle late responses and close their handles.

For large bodies, limit accumulation, decode cautiously, and yield in an appropriate worker without disrupting the main listener. Do not claim fixed chunk sizes guarantee responsiveness on every runtime.

## WebSockets and audio

Own each socket's lifecycle and route URL/connection-specific events correctly. Handle close/failure and bounded reconnect, not an endless busy retry. Keep authorization material out of logs.

For streamed audio, decode DFPWM with the installed `cc.audio.dfpwm`, respect speaker backpressure, and wait for the matching speaker's `speaker_audio_empty` event before retrying a rejected buffer. Test stop, disconnect, and response/socket cleanup paths.
