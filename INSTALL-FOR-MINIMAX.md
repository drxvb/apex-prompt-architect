# Installing APEX Prompt Architect for MiniMax CLI

> **Status:** MiniMax CLI install assumed to follow the same `.skill` ZIP import flow as Claude Code. Verify against your local MiniMax CLI version — if the import command differs, please open an issue.

## Standard install (assumes `.skill` ZIP support)

1. Download the latest `apex-prompt-architect-vX.Y.Z.skill` from [Releases](../../releases).

2. Import via your MiniMax CLI's skill import command (consult your MiniMax CLI docs for the exact command — it's typically something like `minimax skills import <path>`).

3. Configure the LLM endpoint:

   ```bash
   export LLM_API_URL=https://api.minimax.chat/v1/text/chatcompletion_v2
   export LLM_API_KEY=...
   export LLM_MODEL=MiniMax-Text-01
   ```

   Or copy `config.example.json` to `config.json` and edit the `minimax` block.

## Manual install (fallback if `.skill` import isn't supported)

1. Clone the repo:
   ```bash
   git clone https://github.com/drxvb/apex-prompt-architect.git
   ```

2. Tell MiniMax to load the system prompt from the skill:
   ```
   Load the system prompt from ./apex-prompt-architect/prompts/apex-prompt-architect/for-minimax.md
   and apply it to my next request.
   ```

3. Paste your rough prompt and follow the conversation.

## Verifying the install

```bash
python apex-prompt-architect/evals/test_known_fragility.py
# Expected: 10+/10+ passed
```

## MiniMax-specific tuning notes

When using APEX with MiniMax, the default output mode is `standard` but with these MiniMax-aware adjustments built in:

- **Compact prompt is preferred over Detailed** — MiniMax handles tight prompts better
- **Verification blocks are suppressed by default** — MiniMax often produces meta-commentary instead of a clean answer
- **CoT scaffolding is suppressed by default** — over-prompts MiniMax

If you specifically want the Detailed Claude-style scaffolding on MiniMax (rare), pass `--mode deep` to `apex_workflow.py`.
