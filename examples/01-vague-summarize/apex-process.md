# APEX 4D walkthrough — example 01

## Rough input
> i need a prompt that summarizes scientific papers for me

## D1 — Deconstruct

```yaml
intent: summarize scientific papers
task_type: summarize
audience: unspecified → default "general technical reader"
domain: scientific research (broad)
constraints: none stated
success_criteria: implied — faithful, structured summary
output_format: unspecified → default markdown
target_platform: unspecified → default claude
language: en
```

## D2 — Diagnose (failing checks)

- ❌ **Role assigned** — no role
- ✅ **Task verb explicit** — "summarize" present
- ❌ **Audience defined** — no audience indicator
- ❌ **Context boundaries** — no scope (whole paper? specific sections?)
- ❌ **Output format** — no structure specified
- ❌ **Constraints** — no length, vocabulary, exclusions
- ⚠️ **Examples** — would help (no few-shot)
- ❌ **Failure modes** — no fallback for malformed input
- ❌ **Verification** — no self-check
- ⚠️ **Platform length** — to be set per target
- ❌ **Tone** — no register specified
- ⚠️ **Safety** — N/A (creative-writing scope)

## D3 — Develop

Fix targets and applied techniques:

| Fix target | Technique applied |
|---|---|
| Missing role | "senior research scientist comfortable across STEM" |
| Audience unclear | "general technical reader (no specialist jargon assumed)" |
| Open scope | Add explicit 5-section template: TL;DR · Methods · Findings · Limitations · Citations |
| No length | Add `≤ 500 words` constraint |
| No exclusions | Add "do not add information not in the paper" |
| No verification | Add 3-point self-check on faithfulness |
| Tone | "analytical, hedged where warranted" |

Platform tuning: applied for Claude (XML), Kimi (markdown + numbered steps), MiniMax (tight collapse).

## D4 — Deliver

See `OUTPUT-claude.md`, `OUTPUT-kimi.md`, `OUTPUT-minimax.md`.

## Quality check (final, post-D3)

- ✅ Role assigned — senior research scientist
- ✅ Task verb explicit — summarize
- ✅ Audience defined — general technical reader
- ✅ Context boundaries — focus on methods + findings + limitations
- ✅ Output format — 5-section markdown template
- ✅ Constraints — ≤500 words, no external knowledge, no methodology editorializing
- ⚠️ Examples — skipped (task is standard for the domain)
- ✅ Failure modes — "if paper lacks methods section, flag and continue"
- ✅ Verification — confirm every claim traces to a section
- ✅ Platform length — within target for each variant
- ✅ Tone — analytical, hedged where warranted
- ⚠️ Safety — N/A (no PII / auth / legal / medical)
