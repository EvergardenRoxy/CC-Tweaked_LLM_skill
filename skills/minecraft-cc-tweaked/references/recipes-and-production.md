# Effective recipes and production control

[Core](../SKILL.md) · [Create with AP](mod-create-ap.md) · [Recovery](state-and-recovery.md)

## Confirm the recipe before deriving control

A mod jar, wiki, remembered recipe, or earlier test only describes a starting point. Modpacks can replace recipes, change what a tag contains, change outputs or chances, and alter processing conditions through datapacks, scripts (such as KubeJS), configuration, or other mods. A recipe bundled in a jar says nothing certain about the current server.

Build a recipe profile from **what is actually in effect now**. Prefer a recipe export from the server or the pack's final recipe data. A recipe viewer such as JEI/EMI is good corroboration, but confirm hidden conditions and how chances work when unclear. A small trial shows observed behavior but cannot prove an exact probability. CC:T has no recipe API; do not invent one unless an installed mod provides it.

Record:

| Profile field | Evidence needed |
|---|---|
| Environment and source | Pack/server, relevant versions, recipe ID if known, where it came from and when it was checked |
| Inputs | Item IDs or resolved tags, accepted variants, quantities |
| Ordered steps | Machine or process, extra inputs, what each step consumes, routing |
| Repetition | Actual loop count, and at which point the final result is decided |
| Intermediate progress | Readable components/state or another reliable signal; what to do when unknown |
| Outputs | Products, quantities, byproducts, handling of unexpected output |
| Probability, if any | The current recipe's weights or chances; leave unknown if unverified |
| Physical conditions | Heat, fluids, power, speed, accessible slots, how to pause |
| Limits and completion | Target delivered count, attempt and material budget, destination capacity |

Leave unknown fields unknown. For an explanation or display, describe the uncertainty. For automatic feeding, wait until the fields needed to act safely are confirmed. When the profile changes, work in progress may no longer match it: stop new feed and reconcile before resuming.

## Precision mechanisms as a worked method

Do not hardcode a familiar ingredient list, loop count, success rate, or list of failure outputs as the precision-mechanism recipe for every pack. The reviewed Create jar contains a default recipe; its exact values are audit findings and can be used only after confirming they match the current pack.

Derive the controller from the confirmed profile:

1. Use the user's actual layout. One work surface with a shared deployer needs the extra inputs fed in stages; a belt loop or one deployer per step needs different routing and interlocks. Neither layout is required.
2. Start from a clean state. Confirm the input, where processing happens, the extra-input inventory, the output destinations, and that no unexplained leftovers remain.
3. For each confirmed step and repetition, save the intended action when recovery matters, supply only the allowed amount of material, and observe that it was consumed and what resulted before moving on.
4. Use a reliable progress signal: an intermediate item's ID may stay the same across steps. If progress cannot be read and an interruption makes the next step unclear, pause and reconcile.
5. Classify the final output against the verified profile. Move unexpected output aside. Keep products, byproducts, abandoned intermediates, and unresolved work separate.
6. Transfer and count the products actually delivered. Stop at the delivered target or the attempt/material limit, and show why the line stopped: shortage, full output, or too many failures.

A known probability is for planning, not accounting: expected yield is not delivered yield. A success rate may apply to the final result rather than each step; confirm how the recipe works before using it. Never add expected values to a production counter or assume independent trials without evidence.

## Pausing and restarting

Stopping the extra-input feed, disengaging a clutch, and setting speed to zero have different effects. A machine may already hold an input and finish one more action. Cutting shared rotation can also stop displays or other machines. Use the method the user allowed and observe exactly where it stops.

Restart from the saved ledger plus the observed world, not a saved step counter alone. Handle interruptions between the last input being consumed, the output appearing, its transfer, and recording it. If an action may already have happened, do not repeat it blindly.

## Acceptance cases

Test the current profile's full sequence, alternative allowed ingredients, final products and byproducts, unexpected output, and the configured limits. Cover shortages before and during work, partial or zero transfers, full destinations, disconnection, save failure, and a recipe change. Test each relevant interruption point separately.

Do not expect a small test's output ratio to match a nominal probability. A default recipe or scripted responses do not validate the user's current pack.
