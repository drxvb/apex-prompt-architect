# 08 — The 12-Point Quality Checklist

The validator that runs during D2 (Diagnose) and produces the Quality Check section in D4 (Deliver).

## How to read this

Each point has a question (Y/N/⚠️), a quick-fix recipe, and a "skip if" condition. The skill outputs one line per point in the final Quality Check section.

---

## 1. Role assigned

**Question:** Does the prompt include a specific role with seniority or expertise marker?

**Pass:** `"You are a senior security engineer with 10+ years..."`
**Fail:** `"You are a helpful assistant."` or no role line at all

**Quick fix:** Add a role line with: domain + seniority + tone marker.
**Skip if:** task is genuinely role-agnostic (e.g., "list five colors")

---

## 2. Task verb explicit

**Question:** Does the prompt use a concrete action verb?

**Pass:** identify, extract, classify, compare, generate, transform, summarize
**Fail:** help with, work on, do, look at

**Quick fix:** Replace the weak verb with the concrete one.
**Skip if:** never — every prompt needs a task verb

---

## 3. Audience defined

**Question:** Does the prompt say who reads the output?

**Pass:** "for a general technical reader who hasn't read the paper"
**Fail:** no audience indicator

**Quick fix:** Add audience descriptor in the role line.
**Skip if:** task is internal (no human reader — e.g., classification for downstream code)

---

## 4. Context boundaries set

**Question:** Does the prompt say what to include AND what to exclude?

**Pass:** "Focus on the methods section; do not address the conclusions."
**Fail:** open-ended scope

**Quick fix:** Add a `Focus on X; do not address Y` line.
**Skip if:** task is genuinely unbounded (e.g., "summarize this")

---

## 5. Output format specified

**Question:** Is the desired output shape concrete (template, schema, or example)?

**Pass:** explicit markdown template with headers, JSON schema, or one worked example
**Fail:** "format the output nicely" or no format guidance

**Quick fix:** Add a template or example.
**Skip if:** never — every prompt needs a format spec

---

## 6. Constraints stated

**Question:** Are hard requirements explicit (length, tone, vocabulary)?

**Pass:** "≤500 words, no jargon without gloss, no claims not in the source"
**Fail:** no constraints

**Quick fix:** Add 2-3 constraint bullets.
**Skip if:** task is so simple no constraints are needed

---

## 7. Examples present where useful

**Question:** Are 1-3 few-shot examples included when the task is non-trivial?

**Pass:** examples in input → output format
**Fail:** missing examples for a novel task

**Quick fix:** Generate 1-2 examples covering the variation expected.
**Skip if:** task is standard for the domain (model's prior is reliable)

---

## 8. Failure modes addressed

**Question:** Does the prompt say what to do when input is ambiguous or missing?

**Pass:** "If the input lacks X, return Y and flag the gap"
**Fail:** no fallback behavior specified

**Quick fix:** Add an "If unsure / If unavailable" clause.
**Skip if:** task has no plausible failure modes (rare)

---

## 9. Verification step included

**Question:** Is there a self-check before the model responds?

**Pass:** explicit "before answering, confirm X, Y, Z"
**Fail:** no verification

**Quick fix:** Add a verification block targeting the most likely failure for this task.
**Skip if:** task is low-stakes and verification would just inflate tokens

---

## 10. Platform-appropriate length

**Question:** Is the prompt sized for the target model?

**Pass:** Claude 200-800 words · Kimi 150-500 · MiniMax 50-200
**Fail:** length way outside the platform's sweet spot

**Quick fix:** trim (for MiniMax) or elaborate (for Claude).
**Skip if:** task complexity legitimately requires a length outlier

---

## 11. Tone/register specified

**Question:** Is the desired voice specified?

**Pass:** "professional but conversational" / "formal academic" / "direct, no hedging"
**Fail:** no tone indicator

**Quick fix:** add one tone descriptor in the role line.
**Skip if:** tone is implicit from role + audience

---

## 12. Safety/compliance notes when warranted

**Question:** For domains where safety matters (auth, payments, medical, legal, PII), are safety clauses included?

**Pass:** explicit "do not generate real credentials" / "this is informational only" / etc.
**Fail:** no safety clauses for a domain that warrants them

**Quick fix:** add a one-line safety clause from `07-safety-and-compliance.md`.
**Skip if:** domain genuinely doesn't warrant (e.g., creative-writing prompts)

---

## Output format

The skill emits the Quality Check section as 12 lines, each starting with ✅ (pass), ⚠️ (warning), or ❌ (fail), followed by the point name and (for fails/warnings) the quick fix or skip rationale.

Example output:
```
## Quality check (12-point)
- ✅ Role assigned — senior research scientist
- ✅ Task verb explicit — summarize
- ✅ Audience defined — general technical reader
- ✅ Context boundaries — focus on methods + findings
- ✅ Output format — 5-section markdown template
- ✅ Constraints — ≤500 words, no external knowledge
- ⚠️ Examples — skipped (task is standard for the domain)
- ✅ Failure modes — "if paper lacks methods section, flag and continue"
- ✅ Verification — confirm every claim traces to a section
- ✅ Platform length — 350 words, on-target for Claude
- ✅ Tone — analytical, hedged where warranted
- ⚠️ Safety — N/A (creative-writing scope, no PII/auth/legal)
```
