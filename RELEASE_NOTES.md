[简体中文](RELEASE_NOTES.zh-CN.md)

# Unreleased

- Reorganized `SKILL.md` (97 to 204 lines) into workflow, rules, execution model, quick reference, common mistakes, delivery format, reference map, and delivery checklist. It restores concrete guidance lost in the v1.3.0 rewrite: the Lua 5.2 syntax limits, dot versus colon (including `io` handles and `vector`), peripheral naming, events discarded while waiting, chunk unloading, version-sensitive features, and a common-mistakes table.
- Corrected the startup rule: CraftOS runs root `startup` and the files in `/startup/` one after another, and an enabled disk startup replaces them.
- Removed the unverified `cc.base64` version entry; the remaining version entries were checked against tweaked.cc.
- Rewrote the README (both languages), contents overview, and installation guide for clarity, and fixed mistranslated Chinese terms.
- Revised all 26 references. Garbled or machine-like sentences were rewritten, and concrete guidance lost in v1.3.0 was restored: beginner input places and errors, server options, `/computercraft` commands and a version table, where Chinese text works and why, monitor layout rules, design constraints and patterns, and real error messages in troubleshooting. Lua examples are unchanged; the generated index headers were updated in `scripts/inspect_mod_jars.py` too.

# v1.3.0 — English skill restructuring and recipe-driven control

The active skill has been rewritten in English and organized around current-environment evidence. This release includes the core and 26 focused references, plus an English default README and a linked Chinese README. Marketplace metadata is updated to 1.3.0.

- Added a recipe-driven production guide. Current pack/server recipes, tags, steps, repetitions, outputs, and probability semantics must be confirmed before control. Precision-mechanism defaults are no longer hardcoded general rules or universal acceptance criteria.
- Replaced repetitive template collections with focused patterns and explicit adaptation boundaries. Removed homemade authentication/hash examples, unbounded destructive retries, and unsupported safety/exactly-once claims.
- Kept reliability lessons: save failure blocks new actions, corrupt production state is preserved, uncertain effects are reconciled, API business results differ from pcall, and accepted work is not silently discarded.
- Corrected startup coexistence guidance, cooperative-scheduling guarantees, native glyph versus UTF-8 transport claims, default-limit assumptions, and test-evidence overclaims.
- Rewrote the Create/AP guides and generated method-index prose in English while retaining reviewed artifact scope, version-specific contracts, inherited/object-method boundaries, and optional dependencies.
- Renamed the former Chinese-text and template references to `text-and-encoding.md` and `patterns.md`. Updated repository entry points and packaging validation. Historical source records remain outside the installed skill.

> [!IMPORTANT]
> **AI production disclosure: CC: Tweaked LLM Skill uses generative AI to assist with content creation, code validation, and documentation.** AI-generated or modified content is reviewed and verified by the project maintainer, who retains final responsibility for its maintenance.

## Documentation correction

The default English README and Chinese README restore the original project presentation: badges, introduction, design philosophy, prominent AI production disclosure, capability table, installation commands, companion-tool guidance, validation, acknowledgments, and license. Outdated versions and unsupported claims remain removed. The v1.3.0 release page now includes complete Chinese and English notes. These documentation corrections do not change the published skill pack or its checksum.

## Validation

Run the commands in [README](README.md#accuracy-and-validation). Static checks, extracted Lua examples, scripted mod boundaries, and game observations establish different claims. The supplied Java mods and the current server's effective recipes are not executed by the documentation example tests.

Local verification of this source revision:

- Core: 97 lines; 26 routed English reference files; all 12 Lua blocks pass Lua 5.2 syntax, selected official-API, and global-variable checks.
- Ten validator regression cases pass, including Unicode data, untranslated prose, missing/escaping links, unbalanced fences, and offline cache behavior.
- cct-run 0.2.4 / CC:T 1.120.2: 22 reliability assertions pass, including save gating, tuple preservation, file open/read/write/close faults, and non-finite configuration values. The dashboard accepts its selected monitor/keyboard inputs and ignores an unrelated monitor.
- Seventeen scripted mod-adapter assertions and trace checks pass for UTF-8 byte tables, row/column order, failed-render retry, AP options, event layout, and nil/false/exception handling. These do not execute the Java mods or validate game physics/rendering.
- Both English indexes reproduce from the reviewed jars; audit metadata is unchanged and wrong-baseline hashes are rejected. Original archived mod bodies and published release text are preserved.
- The prompt pack contains exactly 27 active Markdown files; paths, local references, CRCs, and byte equality with source are verified. Historical archives, audit inputs, and caches are excluded.

[Published release records through 1.2.2](archive/releases/through-1.2.2.md) are preserved in their original language as historical evidence.
