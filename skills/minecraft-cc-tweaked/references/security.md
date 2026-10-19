# Security boundaries

[Core](../SKILL.md) · [Networking](networking.md)

Use this page when the task includes authentication, untrusted commands, external services, or protecting consequential actions. Do not add a login system to an ordinary trusted local script without a requirement.

## Define what must be protected

Identify who can interact with chat/network inputs, edit computer files, access disks, break/place blocks, issue server commands, or inspect the host. An application password screen cannot prevent a player with sufficient physical/server access from replacing the program or reading its stored secrets.

Ctrl+T suppression, an endless `pcall` loop, hidden messages, a rednet protocol name, and a computer-ID allowlist are not secure authentication. Error handling should not accidentally expose a privileged shell, but preventing termination is not a substitute for an access-control boundary.

## Consequential remote commands

Validate schema, allowed operations, parameter bounds, and authorization separately. Bind a verified identity to the request; reject stale/replayed messages using a defined nonce/sequence policy when necessary. Persist deduplication if restart must not replay accepted commands. Log minimal audit fields rather than credentials or whole requests.

Use reviewed cryptographic implementations/protocols appropriate to the installed runtime and an explicit key-management model. This skill does not provide a homemade password hash, challenge-response protocol, or encryption primitive. A toy hash, `math.random` token, or plaintext password over rednet is not a secure replacement.

For external services, prefer an established authenticated HTTPS endpoint when appropriate. Keep credentials scoped, configurable, and out of release archives, URLs, logs, and screenshots. Ordinary computer files are not protected secret storage against someone who can read them.

Downloaded code executes with the application's privileges. Pin and verify releases from a trusted source; inspect permissions and do not treat sandboxing via an empty `load` environment as a complete defense against resource exhaustion or harmful integration behavior.
