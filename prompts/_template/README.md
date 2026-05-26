# `_template/` — How to add a new prompt to this library

Every prompt in `prompts/` follows this structure:

```
prompts/<your-prompt-name>/
├── README.md           # Purpose, when to use, when not to use
├── for-claude.md       # Claude-tuned variant (XML, long-context)
├── for-kimi.md         # Kimi-tuned variant (markdown, numbered steps)
└── for-minimax.md      # MiniMax-tuned variant (tight, direct)
```

## To create a new prompt

1. Copy this `_template/` directory to `prompts/<your-prompt-name>/`
2. Edit `README.md` — describe purpose + when to use
3. Edit each `for-<platform>.md` — apply the APEX 4D method using the wrapper templates in `../../templates/for-<platform>.md`
4. Run `python ../../scripts/validate_prompt.py prompts/<your-prompt-name>/for-claude.md` (and for kimi/minimax)

## Naming convention

- Use **kebab-case** for directory names: `code-review`, `data-extraction-json`, `arabic-prompt-optimizer`
- The directory name should be a noun phrase describing the prompt's role, not its action
  - ✅ `role-assigner` (this prompt IS a role-assigner)
  - ❌ `assign-roles` (sounds like a CLI command)

## What goes in `README.md`

A short, scannable description (≤ 30 lines):

- **Purpose** — one sentence
- **When to use** — 2-3 bullets
- **When NOT to use** — 1-2 bullets
- **Composes well with** — references to other prompts in this library (if any)
