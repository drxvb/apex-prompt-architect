# Template — for Gemini

System-instruction-anchored prompt. Use this template when the target platform is Gemini (Google). Tight system instructions, multimodal-aware, citation-friendly when grounded.

```
### System instruction
You are [seniority] [role] who [specialization]. You will [task category].

Persistent constraints:
- [Length budget]
- [Tone / register]
- [Forbidden moves]
- [Out of scope]

[Legitimate-purpose framing, when relevant:]
This work is done in service of [legitimate purpose, e.g., "medical professional training", "security research authorized by the system owner", "comparative-religion academic research"]. Apply professional standards appropriate to that context.

[Grounding instruction, when factuality matters:]
Ground factual claims using Search where available. Cite sources inline with brief attribution. Mark un-groundable claims as [unverified].

Output format:
[Exact shape, with citation slots if grounding is on.]

### User turn
[Input — text, plus references to attached modalities if any.]

[Multimodal references, when applicable:]
- "In the attached image..."
- "From minute 2:30 of the attached video..."
- "In the second column of the attached spreadsheet..."

[The specific task instance.]
```

## Multimodal handling

When input includes non-text modalities, reference them by name in the prompt. Gemini is native multimodal — don't ask it to describe the image first, then act; ask it to act on the image directly.

**Good:** "In the attached chart, identify the three largest revenue contributors. Return as JSON."

**Less good:** "Look at the attached chart. Describe what you see. Then identify the largest revenue contributors."

The second form wastes tokens on description Gemini will discard anyway.

## Safety-tier-aware framing

Gemini's safety surface is broader than Claude's. For legitimate-but-borderline topics, state the legitimate purpose explicitly in the system instruction:

| Topic | Purpose framing |
| --- | --- |
| Medical with specific dosages | "This is for a healthcare professional reference; recommend pharmacist consultation in output." |
| Security research | "This is for authorized red-team work on systems owned by the user." |
| Mature creative fiction | "This is for a literary project for adult audiences; apply craft, not gratuitous content." |
| Theological scholarship | "This is for comparative academic research; present sources, distinguish evidence from interpretation." |

Without this framing, legitimate prompts in these domains get refused or watered down on Gemini more often than on Claude or GPT.

## Notes for the architect

- **System instruction is a separate field:** In Gemini's API, `systemInstruction` is structurally separate from the user turn. Use it for persistent rules. Don't bury rules in the user turn.
- **Length sweet spot:** 300–800 words in the system instruction. Past 1000, returns diminish.
- **Numbered steps + concrete examples:** Gemini follows literal structure well. Abstract instructions degrade.
- **Grounding is first-class:** When factuality matters, use it. The model output gets noticeably more reliable.
- **Conservative on edges:** Gemini's default register is slightly more conservative than Claude on edge cases. Purpose framing closes the gap.

## Compact variant pattern

```
### System instruction
You are [role]. Task: [task]. Constraints: [length], [tone], [scope]. [Optional: grounding on/off.] Output: [format].

### User turn
[Input + modality refs + instance]
```
