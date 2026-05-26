# `few-shot-builder`

Generate 1-3 calibrated few-shot examples for a target task, in the input → output shape the user wants.

## When to use
- Task is novel or has a non-trivial pattern
- Model's default behavior on the task is wrong
- You want consistent output across many runs

## When NOT to use
- Task is standard for the domain (model's prior is reliable)
- Examples would bias toward one particular sample
