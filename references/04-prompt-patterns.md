# 04 — Prompt Patterns

The techniques the skill applies in D3. Each is a small, named pattern with a clear use case.

## Few-shot

Show 1-3 worked examples in the input → output shape you want.

**Use when:** The task pattern is non-trivial, the output format is novel, or the model's prior is wrong.

```
Example:
Input: "the meeting is at 3pm tomorrow"
Output: {"event": "meeting", "time": "15:00", "date": "tomorrow"}

Input: "lunch with sarah next thursday"
Output: {"event": "lunch", "attendee": "sarah", "date": "next thursday"}

Now process: <user input>
```

## Chain of Thought (CoT)

Tell the model to think step-by-step *before* answering.

**Use when:** Reasoning-heavy tasks (math, logic, multi-step inference).
**Avoid on:** MiniMax (over-prompts), simple factual tasks (wastes tokens).

```
Before giving the final answer, think step-by-step:
1. What is the question really asking?
2. What information do I have / need?
3. What's my reasoning chain?
4. What's the final answer?

Then provide only the final answer.
```

## ReAct (Reason + Act)

Interleave reasoning and tool calls.

**Use when:** The task requires multiple tool invocations and the model must decide which tool when.

```
For each step:
- Thought: what do I need to know next?
- Action: which tool to call
- Observation: result from tool
- ...repeat until task complete
```

## Tree of Thought

Branch out multiple reasoning paths, evaluate, pick the best.

**Use when:** Tasks with multiple plausible approaches (planning, creative writing, complex math).

```
Consider three different approaches to this problem:
A. <approach>
B. <approach>
C. <approach>

For each, briefly walk through the reasoning. Then evaluate which is most promising and develop it fully.
```

## Self-consistency

Generate multiple answers, take the majority (or best).

**Use when:** Tasks where the model can produce inconsistent answers across runs.
**Note:** Requires multiple inference calls — increases cost.

## Role assignment

See `02-prompt-anatomy.md` §1.

## Structured output (schema-constrained)

Force the model to return JSON matching a schema, or markdown matching a template.

```
Return ONLY valid JSON matching this schema:
{
  "category": "<one of: A | B | C>",
  "confidence": "<float 0-1>",
  "rationale": "<one sentence>"
}
```

**Tip:** Show a worked example matching the schema, not just the schema itself.

## Verification checkpoint

See `02-prompt-anatomy.md` §7.

## Boundary specification (anti-instruction)

Tell the model what NOT to do, in addition to what to do.

```
Do NOT:
- Add information not present in the source
- Editorialize on methodology beyond what the paper itself flags
- Use jargon without a one-line gloss
```

Why this matters: positive instructions alone don't always exclude unwanted behaviors.

## Stepback (zoom-out before zoom-in)

For deeply contextual tasks, ask the model to identify the high-level principle before applying it.

```
Before answering the specific question, identify the underlying principle this is an instance of. Then apply that principle to the specific case.
```

## Pattern composition

Most production prompts compose 3-5 patterns. A typical "code review" prompt might use:
- Role assignment
- Few-shot (one example of good review feedback)
- Boundary specification (don't rewrite — only review)
- Structured output (template with severity tiers)
- Verification checkpoint (every finding cites line number)
