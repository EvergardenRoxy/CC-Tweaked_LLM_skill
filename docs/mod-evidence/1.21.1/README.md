# Reviewed Create / AP artifact evidence

This is development evidence for the Skill repository. It is excluded from the installed skill and `CCT_prompt_pack.zip`; users do not need jars or audit files to load the skill. Active scope is documented in [the baseline](../../../skills/minecraft-cc-tweaked/references/mod-source-baseline.md).

## Inputs and extraction

| Artifact | SHA-256 |
|---|---|
| create-1.21.1-6.0.10.jar | `ef87fe5709f1ba1f5b8bb20a2925b5afb4669e178fd6d8bf10c167759eefe37a` |
| AdvancedPeripherals-1.21.1-0.8.2a.jar | `1bf3e11a1aea4cb4ab024d2fd43261d02565c304a705c6a379e7ebfa4c2d277e` |

[inspect_mod_jars.py](../../../scripts/inspect_mod_jars.py) parses class files without executing the mods. `api-index.json` records artifact metadata, class paths/hashes/parents, Java descriptors, Lua aliases, and main-thread annotations. Create's scan is limited to its ComputerCraft integration namespace; AP's covers its package namespace.

The result is 20 Create classes with 113 annotated method declarations and 62 AP classes with 369 declarations. These include returned objects, parent classes, plugins, and optional integrations, not 482 independent live methods. Runtime registration, dependencies, ownership, configuration, and inheritance still matter.

```bash
python3 scripts/inspect_mod_jars.py \
  --create /absolute/path/to/create-1.21.1-6.0.10.jar \
  --ap /absolute/path/to/AdvancedPeripherals-1.21.1-0.8.2a.jar
```

The script rejects inputs whose hashes differ from the reviewed baselines. A new input requires semantic review as well as changed version text/hash. Generated English method indexes must reproduce from these same artifacts.

## Implementation findings and boundaries

CFR 0.152 reconstructed selected Java implementation in ignored caches. JDK 21 `javap` independently checked selected signatures/behavior. Earlier independent review matched all 482 annotated declarations, aliases, and main-thread flags against decompiled declarations. Reconstructed Java is not supplied upstream source; missing dependencies can distort local decompiler types.

The bundled Create resource `data/create/recipe/sequenced_assembly/precision_mechanism.json` uses a gold-plate tag, cogwheel/large-cogwheel/iron-nugget-tag sequence, five repetitions, and success weight 120 out of total 150. ProcessingOutput Codec defaults explain omitted weights. **These are findings about this jar only, not the effective recipe, loop count, or success probability of an arbitrary modpack/server.** No final server recipe-manager export was provided. The active guide deliberately does not encode these values as production assertions; see [effective recipes](../../../skills/minecraft-cc-tweaked/references/recipes-and-production.md).

The reviewed AP jar uses `chat_box`, options-table sending with an explicit UTF-8 path, and UUID-first chat events. Its artifact chat cooldown default is 1000ms; current server configuration can replace it. Historical tests used different contracts/defaults and are not evidence that this binary was game-tested.

AP's Create integration registers five generic-source groups: Basin, BlazeBurner, FluidTank, FilteringBehaviour, and ScrollValueBehaviour. Actual method merging still depends on the runtime/provider priority and loaded blocks.

Historical processing/reliability lessons come from [MCP joint-test report at 88c3e77](https://github.com/EvergardenRoxy/CC-Tweaked_MCP/blob/88c3e7721d334426e01155abafa8e1cec335cb86/docs/testing/reports/05-precision-mechanism.md). Old prompts, installation choices, permissions, recipes, and skipped tests are scenario evidence rather than universal instructions.

## Verification

The current validation commands and results are recorded in [release notes](../../../RELEASE_NOTES.md). Static checks compile active Lua examples; extracted-example tests retain the documented code and inject only at external boundaries. Scripted mod responses/events do not execute AP/Create Java code, render a real mod target, or process materials in Minecraft.

Raw jars, reconstructed Java, tool binaries, and private session attachments are excluded from repository deliverables and the prompt pack. Historical originals remain separate from active English guidance.
