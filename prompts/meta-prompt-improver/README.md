# `meta-prompt-improver`

Targeted: applies D2 + D3 of the APEX 4D method to a prompt that's *already mostly good* but has 1-3 specific weaknesses.

## When to use
- User has a working prompt and wants polish, not redesign
- One specific aspect needs fixing (output format, verification, role line)
- Quick iteration cycles where you don't want the full 4D walkthrough

## When NOT to use
- The rough input isn't a prompt yet (use `apex-prompt-architect` for full 4D)
- The user wants compare-across-platforms (use `multi-platform-comparator`)

## Composes well with
- `verification-injector`, `output-formatter`, `boundary-setter` (each fixes one specific gap)
