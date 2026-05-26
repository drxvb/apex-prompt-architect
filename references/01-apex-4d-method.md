# 01 — The APEX 4D Method

A deterministic, repeatable workflow for taking any rough prompt and producing a production-quality result. Four phases, in order, no skipping.

## D1 — Deconstruct

**Goal:** Convert prose into a structured intent record.

Read the rough prompt and extract these fields. If a field is missing, mark it as `unspecified` — don't guess yet. Guessing happens in D3 with declared assumptions.

```yaml
intent:           # one sentence — what does the user actually want?
task_type:        # summarize | transform | generate | analyze | extract | classify | roleplay | interview | plan
audience:         # domain expert | general | executive | child | technical reviewer
domain:           # engineering | legal | medical | creative | marketing | research
constraints:      # word limit, format, forbidden words, tone — anything load-bearing
success_criteria: # what "good" looks like (often inferred from context)
output_format:    # markdown | JSON | table | code | narrative
target_platform:  # claude (default) | kimi | minimax
language:         # match input — never auto-translate
```

**Failure modes to avoid in D1:**
- Don't synthesize what the user "probably wants" — extract only what's stated or unmistakably implied.
- Don't classify into `task_type` if it's genuinely ambiguous; mark `task_type: ambiguous` and flag it as a clarification candidate.

## D2 — Diagnose

**Goal:** Identify every gap between the rough prompt and a production prompt.

Run the **12-point quality checklist** (full version in `08-quality-checklist.md`). Each ❌ becomes a fix target. Each ⚠️ becomes a conditional fix (apply if the task warrants).

Output of D2 is a list of fix targets:

```
fix_targets:
  - role_assigned: ❌  → add senior role with audience markers
  - task_verb_explicit: ✅
  - audience_defined: ❌  → infer "general technical reader" (declare in Assumptions)
  - output_format: ❌  → add markdown template with section headers
  - verification: ⚠️    → add for high-stakes domains; skip for casual tasks
  ...
```

## D3 — Develop

**Goal:** Apply prompt-engineering techniques to address every fix target, then platform-tune.

Two passes:

### Pass 1: Address fix targets (platform-agnostic)
Use the technique map from `04-prompt-patterns.md`. Each fix target has a canonical technique.

### Pass 2: Platform adaptation (platform-specific)
Apply `03-platform-adaptation.md` rules:
- **Claude:** XML structure, reflection cues, explicit safety boundaries
- **Kimi:** Markdown headers, numbered task decomposition, self-check sections
- **MiniMax:** Tight role+task opening, minimal scaffolding, list/table output

D3 is the most LLM-sensitive phase. The deterministic D1+D2+D4 path runs offline; D3 enrichment may invoke an LLM (with `temperature=0` for reproducibility) when configured.

## D4 — Deliver

**Goal:** Emit the artifact in the user-requested shape.

**Standard mode output:**
```markdown
# Optimized Prompt — <title>
**Target:** <platform> · **Mode:** standard · **Language:** <lang>

## Detailed prompt
<full multi-section prompt>

## Compact prompt
<one-paragraph compressed version>

## Assumptions applied
- <each smart default the skill picked>

## Usage notes
- <when to use compact vs detailed>
- <known edge cases>

## Quality check (12-point)
- ✅ Role assigned
- ✅ Task verb explicit
- ...
```

**Deep mode adds:**
- D1 intent record (the YAML above)
- D2 fix-targets list
- Three-platform comparison side-by-side
- Risk analysis: what could go wrong with this prompt

## Why "4D" and not "3D" or "5D"?

- **D1 alone** (Deconstruct) is requirements gathering — doesn't improve anything.
- **D2 alone** (Diagnose) is critique — doesn't fix anything.
- **D3 alone** (Develop) without D1/D2 = generic prompt boilerplate that misses what THIS user needed.
- **D4 alone** (Deliver) is just formatting.
- A **5th D** (Deploy? Debug?) tempts scope creep — that's runtime monitoring, not prompt design.

The four phases are minimal-sufficient for the prompt-design problem.
