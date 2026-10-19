[简体中文](RELEASE_NOTES.zh-CN.md)

# v1.3.1 — Documentation correction and restored guidance

v1.3.0 rewrote the skill in English, but the rewrite left many sentences garbled or machine-like and dropped much of the concrete CC:T knowledge the earlier Chinese skill contained. This release fixes the wording throughout and restores that knowledge while keeping v1.3.0's evidence and production-safety rules. The skill structure (core plus 26 references) and the Lua examples are unchanged. Marketplace metadata is updated to 1.3.1.

## Core `SKILL.md`

- Reorganized (97 to 204 lines) into workflow, rules, execution model, quick reference, common mistakes, delivery format, reference map, and delivery checklist.
- Restored concrete guidance: Lua 5.2 syntax limits and missing functions, dot versus colon (including `io` handles, `vector`, and string methods), side and network peripheral names, results that fail without raising errors, events discarded while waiting, sparse inventories and name-string transfers, turtle fuel and `"unlimited"`, chunk unloading, a version-sensitive feature table, and a common-mistakes table.
- Corrected the startup rule: CraftOS runs root `startup` and the files in `/startup/` one after another, and an enabled disk startup replaces them, so adding a file under `/startup/` does not run beside a long-running launcher.
- Removed the unverified `cc.base64` entry; the remaining version entries were checked against tweaked.cc.

## References

- Rewrote garbled or machine-like sentences in all 26 references, for example "No connection implies invented methods" in the Create guide and "Do not claim testing or repeatedly promote optional tools" in the testing guide.
- Restored lost material:
  - Getting started: the shell, `lua` prompt, and editor; how to read signatures; external-editor save paths; beginner errors.
  - Configuration and versions: common server options (marked as defaults to verify), `/computercraft` commands, datapack ROM extensions, the version table, and the Lua compatibility table.
  - Text and encoding: where Chinese text works and why, at the byte level, with glyph libraries as an option that has prerequisites.
  - UI design: monitor layout rules learned from user feedback.
  - Design: CC's hard constraints, five failure questions, the pattern list, and how to review code.
  - Troubleshooting: real error messages such as `attempt to index nil` and `attempt to call nil`.
- Added concrete details to peripherals, the API guide, networking, and turtles, such as wired-modem setup, `fs` versus `io` handle syntax, GPS host requirements, and closing HTTP error responses.
- Where a rewrite would have stated more than the reviewed evidence supports, the original scope was kept.
- The generated method-index headers were reworded in `scripts/inspect_mod_jars.py` as well, so the indexes still match the generator.

## Repository documentation

- Rewrote both READMEs, the contents overview, and the installation guide. Fixed mistranslated Chinese terms such as "活动 Skill" and "附件基线".
- Moved the v1.3.0 notes to the [archive](archive/releases/v1.3.0.md).

> [!IMPORTANT]
> **AI production disclosure: CC: Tweaked LLM Skill uses generative AI to assist with content creation, code validation, and documentation.** AI-generated or modified content is reviewed and verified by the project maintainer, who retains final responsibility for its maintenance.

## Validation

- `validate_skill.py`: core 204 lines, 26 routed references; all 14 Lua blocks pass Lua 5.2 syntax, selected official-API, and global-variable checks.
- `test_validator.py`: all 10 regression cases pass.
- `package_skill.py`: the prompt pack contains exactly 27 Markdown files; paths, CRCs, and byte equality with the source are verified.
- The Lua example bodies are unchanged from v1.3.0. The cct-run example suites (22 reliability assertions, 17 mod-adapter checks) were not re-run for this release.

Earlier notes: [v1.3.0](archive/releases/v1.3.0.md) · [through 1.2.2](archive/releases/through-1.2.2.md).
