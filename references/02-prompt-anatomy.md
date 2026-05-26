# 02 — Prompt Anatomy

The 8 components of a strong prompt. Each component is independent — you can have 8 out of 8 and still have a weak prompt if any single one is poorly written, but a prompt that's missing 3+ components is almost always rescuable by adding them.

## 1. Role assignment

Tells the model who it's pretending to be.

❌ Weak: `"You are a helpful assistant."`
✅ Strong: `"You are a senior security engineer with 10+ years of experience auditing financial-services code. You communicate directly, surface risks early, and never sugar-coat findings."`

Why it matters: roles activate domain-specific knowledge and tone. A vague role gets vague output.

## 2. Context

Background the model needs to do the task — including what NOT to know.

❌ Weak: `"Here's some code. Review it."`
✅ Strong: `"<context>This is a Stripe webhook handler for a SaaS application. It runs in AWS Lambda. The codebase uses TypeScript strict mode. Existing tests use Jest.</context>"`

Context boundaries matter as much as inclusions: "Do not consider performance optimization in this review" is a context narrowing.

## 3. Task (the verb + object)

The single most important sentence. Use an explicit action verb.

❌ Weak: `"Help with this."`
✅ Strong: `"Identify security vulnerabilities in the pasted code, ranked by exploitability."`

Strong verbs: identify, extract, classify, compare, generate, transform, summarize, refactor. Weak verbs: help, do, work on, look at.

## 4. Output format

Concrete shape. Show, don't tell.

❌ Weak: `"Format the output nicely."`
✅ Strong:
```
Return your findings as:
## 🔴 Critical (exploitable now)
- **<vuln name>** at line <N>: <one-line description>

## 🟡 Warning (exploitable with effort)
- ...

## 🟢 Hardening (defense in depth)
- ...
```

## 5. Constraints

Hard requirements. The model will follow these *if you state them*.

- Length: `"≤ 300 words total"`
- Vocabulary: `"Use plain English; no security jargon without a one-line gloss."`
- Forbidden: `"Do not propose fixes — only identify issues."`
- Required: `"Include the line number for every finding."`

## 6. Examples (few-shot)

One or two worked examples when the pattern is non-trivial. The model learns from concrete I/O pairs faster than from abstract description.

When to include: novel task, ambiguous format, or domain where the model's prior is wrong.
When to skip: task is standard for the domain, or examples would bias the model toward your particular sample.

## 7. Verification step

Self-check before responding. Catches the most common failure mode for *this specific task*.

```
Before responding, confirm:
1. Every finding cites a specific line number.
2. You have ranked findings by exploitability, not severity (these differ).
3. No fix proposals appear — only issue identification.
```

## 8. Safety / boundary instructions

What the model should refuse or redirect.

```
If the user pastes credentials, refuse to process and warn them.
If you cannot determine exploitability with confidence, say so — do not guess.
```

## Component density

You don't need all 8 for every prompt. Heuristic:

| Task type | Minimum components |
|---|---|
| One-shot trivial (joke, greeting) | 3, 4 |
| Standard task | 1, 3, 4, 5 |
| Production agent | 1, 2, 3, 4, 5, 7, 8 |
| High-stakes (legal, medical, security) | All 8 |
