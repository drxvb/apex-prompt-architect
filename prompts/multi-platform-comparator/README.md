# `multi-platform-comparator`

Render the same intent across Claude, Kimi, and MiniMax side by side. Useful when a user wants to see *how much* the optimal prompt differs by platform.

## When to use
- User explicitly asks "what would this look like for Claude vs Kimi vs MiniMax?"
- You're calibrating which platform is best for a given task
- Demo / training context — showing the differentiation matters

## When NOT to use
- Single-platform output is enough (use `apex-prompt-architect` instead)
- User has already chosen a platform (no need to compare)
