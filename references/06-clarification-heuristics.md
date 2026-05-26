# 06 — Clarification Heuristics

When to ask the user a question vs. when to apply a smart default. Asking unnecessarily wastes a turn; not asking when you should produces a wildly wrong prompt.

## The single question rule

If you must ask, ask ONE high-value question. Multiple questions push the cognitive load onto the user.

## Ask vs. assume — the decision criterion

**Ask** when:
- Missing info would force a *fundamentally different* prompt structure
- The user's intent is genuinely ambiguous between two non-overlapping interpretations
- Getting it wrong would cost the user noticeable rework

**Assume (with declared default)** when:
- Missing info has an obvious sensible default (audience: general, format: markdown, etc.)
- The user can easily redirect after seeing your output
- The cost of asking exceeds the cost of one rework cycle

## High-value clarification questions

In rank order of impact:

1. **Target platform** — if not stated and the user's other context doesn't strongly imply one. Skip if you can default to Claude and note it.
2. **Audience** — if the task is explanation/summary and audience is genuinely ambiguous (expert vs. layperson produces very different prompts).
3. **Stakes / domain** — for tasks where domain implies safety requirements (medical, legal, financial vs. casual).
4. **Output length** — only if the user mentioned a constraint with no number ("short" — how short?).
5. **Style reference** — only if user mentioned "tone" without anchoring.

## Low-value questions (avoid)

- "What format do you want?" → default markdown
- "What tone?" → default professional
- "Should I include examples?" → infer from task complexity
- "How long?" → write to fit the task

## Question shape

Use the same compact format every time:

```
One question before I proceed: <specific, single-answer question>
Default if unanswered: <what you'll do otherwise>
```

This lets the user say "go with the default" without typing a full answer.

## Avoiding the "20 questions" anti-pattern

Some prompt engineers ask the user to fill in 8-10 fields before producing anything. This is **wrong** for a skill — it shifts the cognitive work to the user. The skill's value is *making the decisions for them* using smart defaults.

If you find yourself wanting to ask 3+ questions, the rough prompt is genuinely under-specified. Instead of asking, produce a `standard` mode output with declared assumptions for ALL of them, and let the user redirect.

## When to refuse instead of ask

Refuse + redirect when:
- The rough prompt asks for content the skill won't generate (jailbreaks, harmful content)
- The target platform is outside {Claude, Kimi, MiniMax}
- The rough prompt contains credentials or PII that must be removed first

Refusal template:
```
I can't proceed because <specific reason>. To get an optimized prompt, please:
1. <action item>
2. <action item>
```
