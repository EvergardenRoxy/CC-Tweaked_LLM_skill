# Effective recipes and production control

[Core](../SKILL.md) · [Create with AP](mod-create-ap.md) · [Recovery](state-and-recovery.md)

## Confirm the recipe before deriving control

A mod jar, wiki, remembered recipe, or prior test describes a baseline. Modpacks can replace recipes, resolve tags differently, change outputs or probabilities, and alter processing conditions through datapacks, scripts, configuration, or other mods. No bundled recipe is an assertion about the current server.

Build a recipe profile from the **effective current environment**. Prefer a server recipe-manager export or installed pack's final recipe data where accessible. A recipe viewer is useful corroboration; confirm hidden conditions/probability semantics when they are unclear. A controlled trial can establish observed behavior but cannot prove a precise probability from a few outputs. Do not invent an API for querying recipes if no installed tool exposes one.

Record:

| Profile field | Evidence needed |
|---|---|
| Environment and provenance | Pack/server identity, relevant versions, recipe ID if exposed, source and verification date |
| Input predicates | Item IDs or resolved tags, accepted components/variants, quantities |
| Ordered operations | Machine/process type, auxiliary inputs, consumption rules, routing |
| Repetition/branch rules | Actual loop count and where final resolution occurs |
| Intermediate identity/progress | Readable components/state or another reliable observation; uncertainty policy |
| Outputs | Accepted products, quantities, byproducts, any unknown-output handling |
| Probability, if relevant | Current recipe's weighting/chance model; optional if unverified |
| Physical conditions | Heat, fluids, power, speed constraints, accessible slots, pause mechanism |
| Limits and completion | Target delivered count, attempt/material budget, destination capacity |

Unknown fields must stay unknown. For a display-only explanation, describe the uncertainty. For automated feeding, pause until the fields needed to act safely are confirmed. A profile change invalidates assumptions of in-flight work; stop new feed and reconcile before resuming.

## Precision mechanisms as a worked method

Do not encode a familiar ingredient list, repetition count, success percentage, or failure whitelist as a universal precision-mechanism rule. The inspected Create jar contains a bundled example; its exact resource findings belong to the source audit and can only be used after confirming they match the current pack.

Derive the controller from the confirmed profile:

1. Select the user's actual topology. One work surface and a shared deployer requires staged auxiliary feeding; a belt loop or several dedicated deployers requires different routing/interlocks. Neither layout is mandatory.
2. Establish a clean workpiece boundary. Confirm the input, processing location, auxiliary inventory, output destinations, and absence of unexplained leftovers.
3. For each confirmed operation and repetition, persist the intended action when recovery is required, supply only the authorized material amount, and observe consumption/result before advancing.
4. Use reliable progress evidence. An intermediate item's registry name alone may remain unchanged across stages. If progress is unreadable and an interruption makes the next action ambiguous, pause for reconciliation.
5. Observe terminal output and classify it against the verified current profile. Quarantine unknown output. Keep successful products, byproducts, canceled intermediates, and unresolved work distinct.
6. Transfer and count actual accepted products. Continue only until the delivered target or explicit attempt/material limit is reached; expose shortage, capacity, or excessive-failure stops.

A known probability supports planning estimates, not accounting. Expected yield is not delivered yield. A success percentage may apply to final recipe resolution rather than each internal step; confirm the recipe's actual model before interpreting it. Do not multiply nominal chance into a production counter or assume independent trials without evidence.

## Pausing and restarting

Stopping auxiliary feed, disconnecting a clutch, and setting speed to zero have different effects. A machine may already hold an input and finish one more action. Stopping shared power can also affect displays or other machines. Choose the mechanism permitted by the user and establish its observed boundary.

Restart from a ledger plus observed world state, not a saved step counter alone. Cover interruptions between final consumption, output creation, transfer, and settlement. If an action may have happened, avoid blindly repeating it.

## Acceptance cases

Test the current profile's full sequence, alternative permitted ingredients, terminal products/byproducts, unknown output, and configured limits. Cover shortages before and during work, partial/zero transfer, full destinations, disconnection, persistence failure, and recipe/profile change. Test relevant interruption windows separately.

Do not require a statistical output ratio to equal a nominal probability in a small test. Do not label an illustrative default recipe or a scripted response sequence as validation of the user's current pack.
