# 03 — Platform Adaptation Matrix

Same intent, three different shapes. This is the differentiating feature of the skill — choosing the right shape for the target model.

## Adaptation matrix

| Aspect | Claude | Kimi | MiniMax |
|---|---|---|---|
| **Structural syntax** | XML tags (`<role>`, `<context>`) | Markdown headers (`# Role`, `# Task`) | Plain prose, minimal scaffolding |
| **Context handling** | Paste full source documents (200K+) | Paste full documents (128K+) | Reference or summarize first |
| **Task decomposition** | Steps OK; reflection cues encouraged | Numbered steps strongly preferred | One sentence; collapse if possible |
| **Reasoning cues** | "Think step-by-step, then answer" | Numbered steps act as implicit CoT | Avoid — leads to verbose output |
| **Output format** | XML-wrapped or markdown — both fine | Markdown with explicit section headers | Tight lists or short paragraphs |
| **Examples (few-shot)** | Welcome; can be elaborate | Welcome; keep them parallel-structured | Use sparingly; one example max |
| **Verification block** | `<verification>...</verification>` natural | Self-check section at end | Skip — over-prompts the model |
| **Safety boundaries** | Always include explicitly | Include when domain warrants | Include in one line at end |
| **Tone** | Analytical, hedged where appropriate | Practical, action-oriented | Direct, decisive |
| **Typical length** | 200–800 words | 150–500 words | 50–200 words |

## When to NOT cross platforms

Some prompts that work on Claude are *actively harmful* on MiniMax:

- A 600-word Claude prompt loaded as a MiniMax system prompt will produce drift — MiniMax over-fits to the early sentences and forgets the later constraints.
- A `<verification>` block on MiniMax often produces meta-commentary instead of a clean answer.
- XML tags on Kimi don't break anything but waste tokens and signal-to-noise.

If a user pastes a Claude-shaped prompt and asks "why isn't this working on MiniMax?" — the answer is almost always *over-scaffolding*.

## Reverse adaptation: MiniMax → Claude

The reverse is usually safe but underwhelming. A tight MiniMax prompt running on Claude will:
- Work correctly
- Under-utilize Claude's strengths (long context, reflection, structured reasoning)

When upgrading a MiniMax prompt to Claude, add: an `<context>` block (even if short), a `<verification>` block, and explicit reflection cues.

## Adapting to platforms not in this matrix

If a user asks for output for a platform not listed (ChatGPT, Gemini, Llama, etc.), do one of:

1. **Refuse politely**: "This skill supports Claude, Kimi, MiniMax. For other platforms, use a platform-specific tool."
2. **Default to Claude** with a note: "Outputting as Claude-shaped; this may need manual adjustment for <platform>."

Don't silently pretend to know the platform's preferences. The cost of bad adaptation is higher than the cost of refusing.

## Future-proofing

When a platform updates (e.g., Claude 5, MiniMax-Text-02), the structural preferences usually hold but the length budgets shift. Update the **typical length** row first; the rest tends to be stable.
