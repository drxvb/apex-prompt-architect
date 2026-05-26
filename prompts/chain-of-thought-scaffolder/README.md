# `chain-of-thought-scaffolder`

Add a "think step-by-step" reasoning scaffold to a prompt for reasoning-heavy tasks.

## When to use
- Math, logic, multi-step inference
- Tasks where the model gets the right answer wrong by jumping to conclusions
- Tasks where you want to inspect the reasoning, not just the answer

## When NOT to use
- Target is MiniMax (over-prompts; produces verbose output)
- Trivial factual tasks (CoT wastes tokens with no quality gain)
- Tasks where the model's first instinct is reliably correct
