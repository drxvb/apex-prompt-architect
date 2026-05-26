# `verification-injector`

Add a "before answering, confirm X, Y, Z" self-check block to a prompt.

## When to use
- High-stakes domain (legal, medical, security, financial)
- Task has known failure modes worth catching
- Output will be consumed by downstream code or human decisions

## When NOT to use
- Low-stakes casual task (verification block bloats tokens)
- Target is MiniMax (verification often produces meta-commentary)
