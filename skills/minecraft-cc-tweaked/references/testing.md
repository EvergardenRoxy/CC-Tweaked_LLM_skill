# Testing and evidence

[Core](../SKILL.md) · [Recovery](state-and-recovery.md) · [Production](recipes-and-production.md)

## Match the test to the claim

| Layer | Can establish | Cannot establish alone |
|---|---|---|
| Syntax/static checks | Parseability, selected API/global mistakes, document structure | Runtime/world correctness |
| Pure logic tests | State transitions, validation, limits for selected inputs | Device contracts or real scheduling |
| Scripted peripheral boundary | Actual adapter parameters, false/nil/errors, chosen event payloads | Java mod behavior or genuine game events |
| CC:T runtime/simulator | Exercised filesystem, scheduler, core device semantics under its model | Live server configuration, mod rendering/physics |
| Live injected fault/event | Program handling of the injected condition | That the mod naturally emits it or the real fault occurred |
| Actual game observation | Observed behavior of this installation and scenario | Every configuration or untested failure window |

Use available tooling without inventing it. Tools named `cct_run`/`cct_trace` or a local `cct-run` may support fixtures and traces; inspect their current guide/schema. If unavailable, perform the checks possible and state what did not run. Do not claim testing or repeatedly promote optional tools.

## Build a meaningful case

Start from the user's revised conditions and actual device layout. Record versions, recipe evidence, allowed actions, inputs, expected observable result, and stop condition. Keep test data and prompts distinct from user instructions. A skipped case remains skipped.

For mod tests, retain the real adapter and inject at its external boundary. Replacing the adapter with a fake always-true function cannot validate that adapter. Preserve nonzero cooldowns and realistic result shapes when those matter.

Use distinct request IDs for burst tests, verify acceptance/rejection and final handling/reply per ID, then test duplicate IDs separately. Include queue-full behavior. Arbitrarily many assertions or repeated identical commands do not establish many independent end-to-end cases.

## Production regression matrix

Select relevant cases:

- Effective recipe/profile matches the installation; changed recipe/unknown output pauses new feed.
- Complete configured sequence and actual delivered product; no fixed default loop/probability assertions.
- Missing input before start versus during processing; zero/partial transfer and full destinations.
- Device disconnect, stale observation, actual pause boundary, and appropriate stop/resume.
- Main/backup generations, corrupt production state, and intent open/write/close/promotion failures.
- Interruptions around final consumption, result creation, transfer, and settlement as separate windows.
- Business false/nil/error, asynchronous pending/canceled/failed states, and void setter semantics.
- Display size/order, encoding, failed update retry, cache invalidation, and actual visibility.

A short random-production run cannot validate an exact success probability. Use confirmed profile values for planning and actual products for accounting.

## Live work and cleanup

Use an authorized computer and scope. Snapshot affected files/settings before diagnostics; record existing startup and state. Avoid resetting storage, disabling cooldowns, or replacing devices to satisfy a test unless that change is explicitly part of the scenario.

Restore temporary diagnostic changes and release any acquired control/session. Keep the requested installed program and deliverables; do not blindly roll back the very changes the user asked for. Termination/reboot changes program state and can expose different paths; note when the test caused it.

Read trace pages using advancing cursors, retain request IDs/time ranges, and expose truncation or retention gaps. Aggregate complete inventory data before summarizing. Repeatedly fetching an old first page is not ongoing observation.

## Report precisely

Give the resulting behavior, relevant cases and outcomes, runtime/model used, injected versus real events, and remaining boundaries. Separate assertions, scenarios, and independent game cases. A passing old suite does not invalidate a newly reproduced fault.

The repository's documented helper tests run in CC:T without executing the supplied Java mods. Historical lessons originate in [the reviewed joint test](https://github.com/EvergardenRoxy/CC-Tweaked_MCP/blob/88c3e7721d334426e01155abafa8e1cec335cb86/docs/testing/reports/05-precision-mechanism.md); previous test-specific permissions, layouts, recipe values, and skipped cases are not standing requirements for another installation.
