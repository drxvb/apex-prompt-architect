# 03 — Platform Adaptation Matrix

Full tuning rules per platform. Load this file when the SKILL.md summary isn't enough — e.g., when the prompt is non-trivial, when the user asks for a multi-platform comparison, or when a platform-specific feature (JSON mode, multimodal, long-context restate) is in play.

## Quick selection table

| Need                                       | Best platform   | Why                                                       |
| ------------------------------------------ | --------------- | --------------------------------------------------------- |
| Long analytical reasoning, hedged          | Claude          | Reflection-native, XML-aware                              |
| Long-document synthesis (50K–128K)         | Kimi or Claude  | Both handle inline; Kimi cheaper, Claude more accurate    |
| Tight, fast, decisive output               | MiniMax         | No CoT overhead, role+task in line 1                      |
| Structured JSON / tool use                 | GPT             | `response_format` + function-calling are best-in-class    |
| Multimodal grounding + search              | Gemini          | First-class image/video, Google Search grounding          |
| Mature/edgy creative within policy         | Claude          | Cleanest refusals; safety boundaries are explicit         |
| Arabic-first prompts                       | Claude or GPT   | Both handle MSA well; Claude better at register fidelity  |

## Claude (primary target)

**Strengths to lean on:**
- 200K+ token context — paste raw documents inline rather than summarizing first
- XML tags as structural primitives — Claude was trained on `<context>`, `<instructions>`, `<output_format>`, `<example>`, `<thinking>`
- Reflection cues fire natively — "Think step-by-step before answering" actually changes behavior
- Strong instruction-following when the goal is stated as a single clear objective

**Knobs to set:**
- **Structure:** XML tags for any prompt over ~200 words. Use semantic tag names.
- **Reasoning:** Add `<thinking>` scaffold for analytical tasks; let it think before producing.
- **Safety:** State scope boundaries explicitly. Claude refuses cleanly when given them; gets defensive without.
- **Length:** No upper limit pressure. Don't artificially compress — Claude handles long.
- **Tone:** State register explicitly if it matters ("formal academic", "conversational technical"). Defaults to balanced-professional.

**Pitfalls:**
- Don't double-instruct: telling Claude "be helpful AND don't be harmful" is redundant — RLHF already handles it; redundant safety text actually triggers more hedging.
- Don't ask for "be confident" — produces overclaim. Ask for "state confidence levels" instead.
- Don't use ALL CAPS for emphasis — Claude treats it as semantic, not stylistic, and shifts register.

**Template skeleton (use `templates/for-claude.md`):**
```
<role>You are a [specific role with seniority].</role>

<context>
[domain background, what to assume, what to ignore]
</context>

<task>
[explicit action verb + object + qualifier]
</task>

<constraints>
- [length, tone, vocabulary]
- [forbidden moves]
- [verification step]
</constraints>

<output_format>
[exact shape — markdown structure, JSON schema, or example]
</output_format>

<thinking>
Before answering, work through:
1. [decomposition step]
2. [verification step]
</thinking>
```

## Kimi

**Strengths to lean on:**
- 128K context, excellent at document QA and long-form synthesis
- Hierarchical task lists — Kimi follows numbered, nested steps reliably
- Markdown is the native structural language

**Knobs to set:**
- **Structure:** Markdown headers (`##`, `###`) for sections. Numbered lists for steps.
- **Reasoning:** Step-by-step decomposition. Each step gets its own line.
- **Context:** Restate, don't reference. Kimi sometimes loses implicit cross-turn references — make each prompt self-contained.
- **Length:** Concise but COMPLETE. Don't strip context to save tokens; Kimi degrades on incomplete prompts more than it does on long ones.

**Pitfalls:**
- Don't use XML — Kimi tolerates it but doesn't lean on it the way Claude does.
- Don't assume Kimi remembers an earlier turn's setup — restate the role and constraints if anything depends on them.
- Don't ask for free-form reasoning followed by an answer — Kimi sometimes truncates the reasoning. Ask for the answer first, then the reasoning.

**Template skeleton (use `templates/for-kimi.md`):**
```
# Role
[specific role + expertise marker]

# Context
[background, source documents pasted inline]

# Task
[numbered, decomposed]
1. ...
2. ...
3. ...

# Output format
[explicit structure with example]

# Constraints
- [length]
- [tone]
- [forbidden moves]
```

## MiniMax

**Strengths to lean on:**
- Fast execution, low latency, decisive output
- Works well for tight transactional prompts (classify, extract, transform)

**Knobs to set:**
- **Length:** 1–2 paragraphs max in the system prompt. Anything longer dilutes.
- **Opening:** "You are X. Your task is Y." — role and task in the first sentence.
- **Output:** Lists, tables, short paragraphs. Avoid nested reasoning.
- **CoT:** Skip it. MiniMax shines at direct execution.

**Pitfalls:**
- Don't add "think step-by-step" — adds latency without quality gain.
- Don't use XML — overhead without payoff.
- Don't hedge ("if possible", "try to") — MiniMax follows literally; soft requests get soft compliance.

**Template skeleton (use `templates/for-minimax.md`):**
```
You are [role]. Your task is [task in one sentence].

Constraints:
- [bullet]
- [bullet]

Output format:
[exact shape]

[Optional: one example of input → output]
```

## GPT (added in this port — not from upstream)

**Strengths to lean on:**
- Best-in-class function calling and JSON mode
- System message carries strong weight — instructions there are followed more reliably than in user-turn instructions
- Long context restate-after pattern works well (state context first, then question at the end)

**Knobs to set:**
- **Structured output:** If output is structured, specify the JSON schema explicitly. For OpenAI API users, recommend `response_format: { "type": "json_object" }` or a named tool call.
- **System message:** Put role, task category, refusal policy, and persistent constraints in the system message. User turn is for the actual input.
- **Reasoning models (o1, o3, o-series):** Drop CoT scaffolds. The model already reasons. State goal + constraints + success criteria; let it choose the method.
- **Non-reasoning models (GPT-4o, GPT-4.1):** `Let's think step by step` works. Use for analytical tasks.
- **Long context:** Restate the question after the context, not before. ("Above is the document. Now: [question]")

**Pitfalls:**
- Don't mix CoT and reasoning models — wastes thinking budget.
- Don't use XML as primary structure — markdown is native; XML is parsed but doesn't carry semantic weight the way it does in Claude.
- Don't omit a JSON schema when you expect JSON — GPT will sometimes wrap in markdown code fences. Either specify schema strict mode or post-process.

**Template skeleton (use `templates/for-gpt.md`):**
```
### System
Role: [specific role]
Task category: [classify | extract | generate | analyze | transform]
Persistent constraints:
- [bullet]
- [bullet]
Refusal policy: [what to refuse + how]

### User
[input + optional one-shot example]

Output format: [explicit — JSON schema if structured]
```

## Gemini (added in this port — not from upstream)

**Strengths to lean on:**
- Multimodal-native — images, video, audio, PDF are first-class inputs
- Google Search grounding — when factuality matters, the model can ground and cite
- Strong at conservative, citation-friendly output

**Knobs to set:**
- **System instructions:** Dedicated `systemInstruction` field. Keep tight (300–800 words). Place persistent constraints there, not in the user turn.
- **Multimodal:** When input includes non-text modalities, reference them by name in the prompt ("In the attached image…", "From minute 2:30 of the video…").
- **Grounding:** For factuality-sensitive tasks, instruct the model to ground with Search and cite sources.
- **Safety tier:** For borderline-but-legitimate content (medical, security research, mature fiction, theology), state the legitimate purpose explicitly in the system instruction — Gemini is more conservative than Claude on edge cases and benefits from explicit framing.
- **Structure:** Numbered steps + concrete examples. Gemini follows literal structure well.

**Pitfalls:**
- Don't bury system instructions in the user turn — they get less weight.
- Don't assume Gemini will refuse the same edge cases as Claude — Gemini's safety surface is broader; some legitimate medical/legal/security topics get refused without explicit purpose framing.
- Don't ask for long free-form reasoning — Gemini's strength is grounded, citation-style output, not Claude-style essay reasoning.

**Template skeleton (use `templates/for-gemini.md`):**
```
[systemInstruction]
You are [specific role]. You will [task in one sentence].

Persistent constraints:
- [bullet]
- [bullet]

Legitimate-purpose framing (if relevant): [why this work is needed]
Grounding: [yes/no — if yes, cite sources via Search]

[user turn]
[input + modality references + task instance]

Output format:
[explicit structure with citation slots if grounding]
```

## Cross-platform: when the same intent fans out

When the user asks for the same intent rendered across multiple platforms:

1. Run D1–D3 once. The intent record and fix targets are platform-agnostic.
2. At D4, branch: emit one optimized prompt per requested platform, applying the template above.
3. State explicitly in the output what each variant emphasizes differently. Don't make the user diff them.
4. If a target platform is fundamentally a poor fit for the intent (e.g., asking MiniMax for 5-page analytical reasoning), say so in the Usage notes section — don't silently degrade.
