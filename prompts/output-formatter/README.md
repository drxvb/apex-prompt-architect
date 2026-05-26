# `output-formatter`

Add an explicit output-format spec (markdown template, JSON schema, or worked example) to a prompt that lacks one.

## When to use
- Rough prompt says "format the output nicely" or has no format guidance
- Downstream consumer needs a specific shape (UI, parser, evaluation script)
- You want consistency across multiple runs of the same prompt

## When NOT to use
- The format is already concrete and explicit
- The task genuinely has no fixed output shape (creative writing)
