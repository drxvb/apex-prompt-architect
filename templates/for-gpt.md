# Template — for GPT

System-message-anchored prompt. Use this template when the target platform is GPT (OpenAI). Strong system message; structured output when possible; JSON schema explicit if downstream parsing.

```
### System message
You are a [seniority] [role] who [specialization].

Task category: [classify | extract | generate | analyze | transform | reason]

Persistent constraints:
- [Length budget]
- [Tone / register]
- [Forbidden moves]
- [Out-of-scope topics]

Refusal policy: [What to refuse + how to refuse. E.g., "If asked to produce X, respond with the refusal phrase 'I can't help with that' and offer an adjacent legitimate alternative."]

Output format: [Exact shape. If structured, JSON schema below.]

### User message
[The actual input — content to classify, document to summarize, code to review, etc.]

[Optional one-shot example, when format is non-obvious:]
Example
Input: [...]
Output: [...]

[Restate the question at the end, after long context:]
Now, [the specific instance of the task].
```

## JSON output discipline (when applicable)

When output is structured, specify the schema explicitly in the system message:

```
Output is a JSON object matching this schema:
{
  "field_a": "string — description",
  "field_b": "integer | null — description",
  "field_c": ["array of strings — description"]
}

Return ONLY the JSON object. No markdown fences. No commentary.
```

For OpenAI API users, recommend `response_format: { "type": "json_object" }` or, for stricter typing, a named function call with the schema.

## Reasoning models (o1, o3, o-series) — special handling

For reasoning models, strip CoT scaffolds and verbose decomposition. The model already reasons internally. The pattern becomes:

```
### System message
You are a [role]. You will [task in one sentence].

Constraints: [list]
Output: [format]
Success criteria: [what good looks like]

### User message
[Input]
```

No "Let's think step by step". No `<thinking>` tags. State the goal; let the model choose the method.

## Notes for the architect

- **System message carries weight:** Constraints in the system message are followed more reliably than constraints in the user turn. Move persistent rules there.
- **Markdown over XML:** Markdown is native. XML is parsed but doesn't carry semantic weight.
- **Long-context restate:** State the question AFTER the context, not before. "Above is the document. Now: [question]."
- **JSON mode is your friend:** If output is structured, use it. Or use a named tool call. Don't trust free-form "return JSON" without enforcement.
- **Length sweet spot:** 200–1500 words across system + user.

## Compact variant pattern

```
### System
You are [role]. Task: [task]. Constraints: [length], [tone]. Output: [format].

### User
[Input]
```
