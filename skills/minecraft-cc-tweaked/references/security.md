# Security boundaries

[Core](../SKILL.md) · [Networking](networking.md)

Read this page when the task involves passwords, door locks, permissions, untrusted remote commands, external services, or protecting important actions. Do not add a login system to an ordinary local script unless the user asks. By default, mention the risk in one or two sentences and offer options; add security code only after the user agrees and the threat is defined.

## Define what must be protected

Identify who can send chat or network messages, edit the computer's files, insert disks, break or place blocks, run server commands, or read the server's files. A password screen cannot stop a player who can break the computer, boot it from a disk, or read the world save from replacing the program or reading its stored secrets.

Blocking Ctrl+T (`os.pullEventRaw`), an endless `pcall` loop, hidden chat messages, a rednet protocol name, and a list of allowed computer IDs are not authentication: IDs and protocols can be forged by anyone in range. A crash should not drop the user into a shell on a door computer, but preventing termination does not replace access control.

## Consequential remote commands

Check the message format, the allowed operations, parameter ranges, and authorization as separate steps. Tie each request to a verified identity, and reject old or replayed messages with a nonce or sequence number when that matters. Persist deduplication records if a restart must not replay accepted commands. Log only minimal audit fields, never credentials or whole requests.

Use a reviewed cryptography library suited to the installed runtime, with a clear plan for how keys are created, stored, and replaced. This skill deliberately provides no homemade password hash, challenge-response protocol, or encryption. A toy hash, a `math.random` token, or a plaintext password over rednet is not secure.

For external services, prefer an existing authenticated HTTPS service. Keep tokens narrowly scoped, configurable, and out of release archives, URLs, logs, and screenshots. Files on the computer are readable by anyone with access to it or to the world save.

Downloaded code runs with the program's full permissions. Pin versions and verify them from a trusted source. An empty `load` environment does not protect against endless loops, memory use, or harmful peripheral calls; never `load` received messages.
