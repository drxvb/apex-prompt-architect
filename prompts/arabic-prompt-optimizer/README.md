# `arabic-prompt-optimizer`

Apply the APEX 4D method to an Arabic-language prompt, with MSA register awareness and Arabic typography hygiene.

## When to use
- Rough prompt is in Arabic and the optimized prompt should stay in Arabic
- Rough prompt is an AI-translated English prompt that reads mechanically
- You want a prompt that won't trip on Arabic-specific failure modes (kashida injection, em-dash artifacts, calque translations)

## When NOT to use
- The user explicitly wants the prompt translated to English
- The rough prompt is dialectal Arabic (this skill targets MSA only)

## Composes well with
- The [arabic-ai-text-humanizer](https://github.com/drxvb/arabic-ai-text-humanizer) typography pipeline for cleaning the final output
- `meta-prompt-improver` for targeted Arabic-prompt polish
