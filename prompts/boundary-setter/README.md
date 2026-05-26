# `boundary-setter`

Add "Do NOT do X" guardrails to an over-broad prompt.

## When to use
- Rough prompt has no boundary specifications
- You're seeing the model wander into unwanted territory
- Task has known scope-creep failure modes

## When NOT to use
- The prompt already has tight scope
- The user's intent is genuinely exploratory (boundaries would prevent useful tangents)
