# Remove Mnemonic Plugin Dependency

## Status

Accepted

## Context and Problem Statement

The ADR plugin was originally developed as part of the author's personal Claude Code setup, which included the `mnemonic` plugin — a separate plugin providing `/mnemonic:search`, `/mnemonic:capture`, and `/mnemonic:list` slash commands for persisting structured memories across sessions.

Mnemonic protocol blocks were embedded in every command, agent, and skill file (22 files total), instructing Claude to search and capture memories via mnemonic commands on every invocation. When the ADR plugin is distributed publicly, users will not have the mnemonic plugin installed. The embedded blocks become dead instructions that Claude will attempt to execute but fail silently, and they add noise to every prompt without providing value.

Should the mnemonic protocol blocks be removed for public distribution, or should mnemonic be declared a required dependency?

## Decision Drivers

* The ADR plugin must work correctly for users who have not installed any other plugins
* Undeclared dependencies that fail silently degrade user experience
* The mnemonic commands are not core to ADR functionality — they were a personal productivity enhancement
* Plugin manifests (`plugin.json`) have no mechanism to declare plugin-to-plugin dependencies
* Keeping the blocks would require users to install a second plugin with no clear documentation path

## Considered Options

* Remove all mnemonic protocol blocks from commands, agents, and skills
* Declare mnemonic as an optional dependency and document it in README
* Keep the blocks and accept that they fail silently for most users

## Decision Outcome

Chosen option: "Remove all mnemonic protocol blocks", because it is the only option that guarantees correct, self-contained behaviour for all users without undeclared requirements.

### Consequences

* Good, because the plugin works out-of-the-box for any user without additional setup
* Good, because prompt content is cleaner and focused on ADR functionality
* Good, because there is no silent failure path from unresolved slash commands
* Bad, because users who do have the mnemonic plugin installed lose the memory integration benefit
* Neutral, because mnemonic integration can be re-added in a future release once plugin dependency declarations are supported by Claude Code

### Confirmation

Verified by running `grep -r "mnemonic" commands/ agents/ skills/` returning zero results, and all 22 files confirmed clean. The `tests/validate.py` validation suite continues to pass.

## Pros and Cons of the Options

### Remove all mnemonic protocol blocks

* Good, because self-contained — no external dependencies
* Good, because no silent failures for users without mnemonic
* Good, because reduces prompt noise across 22 files
* Bad, because loses cross-session memory recall for users who had it working

### Declare mnemonic as optional dependency and document it

* Good, because power users retain the memory integration
* Bad, because Claude Code has no formal optional-dependency mechanism
* Bad, because README documentation alone is insufficient to prevent confusion
* Bad, because the blocks still fail silently when mnemonic is absent

### Keep blocks, accept silent failure

* Good, because no code changes required
* Bad, because every command/agent/skill invocation includes broken instructions
* Bad, because unpredictable behaviour depending on whether mnemonic is installed
* Bad, because fails the basic requirement of a self-contained distributable plugin

## More Information

The mnemonic protocol was stripped across all 22 affected files in commit `37c2239` (skills) and `33f7a51` (commands), with the single stray prose reference removed from `agents/adr-author.md` in the same change set. If Claude Code introduces a plugin dependency declaration mechanism in future, mnemonic integration can be re-evaluated.
