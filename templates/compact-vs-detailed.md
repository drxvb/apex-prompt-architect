# Compact vs Detailed — pairing pattern

Every optimized prompt the skill produces comes in two forms. Use this template to choose which to emit (or both).

## When to use the Detailed version

- Production agent system prompts (loaded once, used many times)
- Critical or high-stakes tasks (legal, medical, security)
- Tasks where verification is required
- New domains where the operator is calibrating

## When to use the Compact version

- One-shot user queries (token-budget conscious)
- Iterative experimentation
- Tasks where the user will re-prompt anyway based on output
- Embedded in tool definitions or system messages where space is tight

## Pairing pattern

The Compact form should be a *faithful compression* of the Detailed form — not a different prompt. Test:

> If a user runs the Compact prompt and gets noticeably worse output than the Detailed prompt, the Compact form is over-compressed.

## Compression heuristics

| Detailed element | Compact equivalent |
|---|---|
| Multi-paragraph role with goals + responsibilities | One sentence: "You are X. Your task is Y." |
| `<context>` block with source docs | "Input: <description>" |
| Numbered task decomposition | Single verb + object |
| Output format with worked example | One-line format spec |
| `<verification>` block | Drop (relies on model competence) |
| Few-shot examples | Drop unless task is genuinely ambiguous |

## What to NEVER drop in compression

- Hard constraints (length, format, exclusions)
- Safety / boundary instructions
- The actual task verb

If you're tempted to drop these, the Compact form is invalid — emit only Detailed.
