# 05 — Anti-Patterns

Common prompt-engineering mistakes. Recognize them in rough prompts; avoid them in optimized ones.

## 1. Under-specification

The most common failure. "Help me write something good about X" leaves the model to guess audience, length, format, tone, depth.

**Symptom in rough prompts:** vague nouns and verbs.
**Fix:** explicit role + audience + task verb + output format.

## 2. Role drift

A long prompt where the role shifts mid-way. "You are a security engineer. Also help with marketing copy if I ask." → the model wobbles on every response.

**Symptom:** multiple unrelated personas in one prompt.
**Fix:** one prompt = one role. Use a separate prompt for the second persona.

## 3. Format leak

Asking for one format and accidentally instructing another.

**Symptom:** "Return JSON. Then summarize in 3 paragraphs." (Now the model returns JSON-wrapped paragraphs or paragraphs containing JSON — neither is what you wanted.)
**Fix:** pick one final format. If you need both, ask for them in separate turns or in a schema with both fields.

## 4. Conflicting constraints

"Be concise but thorough." "Avoid jargon but use precise technical language." "Be friendly but formal."

**Symptom:** constraints that pull in opposite directions.
**Fix:** prioritize one explicitly. "Prefer thorough over concise; if you must choose, pick thorough."

## 5. Over-prompting

Adding so much scaffolding that the model spends more tokens on meta-reasoning than on the actual task.

**Symptom:** 500-word system prompt for a "translate this sentence" task.
**Fix:** match scaffolding to task complexity. Trivial tasks get tight prompts.

## 6. Hidden assumptions

"Make it sound natural." Natural to whom? In what register? In which language?

**Symptom:** subjective adjectives without anchoring.
**Fix:** define the standard explicitly or pick a concrete reference ("sound like a New York Times tech reporter").

## 7. Implicit references

"Use the same style as before." (When loaded as a system prompt, "before" doesn't exist.)

**Symptom:** references to context that doesn't survive prompt loading.
**Fix:** state the style explicitly; don't rely on prior conversation.

## 8. Forbidden-word lists that backfire

"Don't use the word 'leverage'." → the model now thinks about 'leverage' and uses synonyms that hit the same problem.

**Symptom:** long lists of banned words.
**Fix:** specify positive style markers instead ("use concrete verbs, avoid corporate jargon").

## 9. Confidence theater

"Be confident in your answer." → the model becomes overconfident and hides uncertainty.

**Symptom:** instructions to project confidence regardless of truth.
**Fix:** "Express confidence calibrated to the evidence. Say 'I don't know' if you don't."

## 10. Anchoring on the wrong example

A few-shot example that's slightly off-domain. The model overfits to it and applies the wrong pattern.

**Symptom:** one example that's similar but not identical to the target.
**Fix:** either give 0 examples (zero-shot) or 2-3 examples that span the variation you expect.

## 11. Format-format mismatch

Asking for markdown but providing JSON as the example.

**Symptom:** the example contradicts the format instruction.
**Fix:** examples must match the requested output format exactly.

## 12. Politeness inflation

"Please could you possibly help me to maybe write a summary if it's not too much trouble?"

**Symptom:** verbal hedging that the model mirrors in output ("Here is a possibly helpful summary that may address your needs…").
**Fix:** direct phrasing in the prompt produces direct phrasing in the output.

## How the skill flags these

In D2 (Diagnose), the 12-point checklist surfaces #1, #3, #4, #6, #11 directly. Patterns #2, #5, #7, #8, #9, #10, #12 are flagged as ⚠️ warnings when detected; the user is told what's risky and what to change.
