# `role-assigner`

Generate a strong role/persona line for an underspecified task.

## When to use
- The rough prompt has "You are a helpful assistant" or no role at all
- The task domain implies a specialist but the prompt doesn't name one
- You want a calibrated seniority + audience + tone marker in one line

## When NOT to use
- The role is already specific (this prompt would just repaint)
- The task is genuinely role-agnostic (e.g., "list five colors")

## Output shape
Returns ONE role line, ready to drop into any prompt as the opening sentence.
