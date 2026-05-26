<!--
Claude wrapper template.
Use when target_platform = claude.

Claude rewards: XML structure, long context, explicit reflection cues, safety boundaries.
Claude penalizes: vague scope, implicit context, missing verification on high-stakes tasks.
-->

<role>
You are <role with seniority marker>. <One-sentence mission>.
</role>

<context>
<Paste relevant source documents inline — Claude handles 200K+ tokens, no need to summarize first.>
</context>

<instructions>
1. <Step 1 — explicit verb + object>
2. <Step 2>
3. <Step 3>

Before answering, think step-by-step about <key uncertainty or decision point>.
</instructions>

<constraints>
- <hard requirement>
- <hard requirement>
- DO NOT: <forbidden behavior>
</constraints>

<output_format>
<concrete template, JSON schema, or worked example showing the exact shape>
</output_format>

<examples>
<one or two few-shot examples — only when the task pattern is non-trivial>
</examples>

<verification>
After drafting, confirm:
1. <check that ties to a specific failure mode>
2. <check that catches the most likely error>
If any check fails, revise before responding.
</verification>
