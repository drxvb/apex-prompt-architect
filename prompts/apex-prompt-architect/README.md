# `apex-prompt-architect` — The skill's own system prompt

The meta-prompt that **IS** this skill. Use it as the system prompt when running APEX inside any agent CLI.

## Purpose

Turns the APEX 4D method + platform-adaptation rules + 12-point quality checklist into a system prompt the model can apply on its own to incoming rough prompts.

## When to use

- You want to drop APEX into a Claude / Kimi / MiniMax agent and have it auto-apply on prompt-improvement tasks
- You want to fork-and-adapt the canonical APEX behavior

## When NOT to use

- You want to run APEX as a deterministic Python pipeline (use `scripts/apex_workflow.py` instead)
- You want a one-shot prompt for a specific narrow task (use one of the other prompts in this library)

## Variants

- `for-claude.md` — XML structure, full 4D walkthrough, long context
- `for-kimi.md` — markdown structure, numbered phases, self-check
- `for-minimax.md` — tight version, role+task collapsed, output template only

## Composes well with

- `meta-prompt-improver` — when you want to apply just D3 to an already-mostly-good prompt
- `multi-platform-comparator` — when you want side-by-side Claude/Kimi/MiniMax variants of the same intent
