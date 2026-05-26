<!--
Kimi wrapper template.
Use when target_platform = kimi.

Kimi rewards: clear markdown hierarchy, numbered task decomposition, document-anchored context, self-check sections.
Kimi penalizes: XML tags (use markdown), implicit cross-turn references, deep nested reasoning.
-->

# Role
You are <role with seniority marker>. Mission: <one sentence>.

# Source Material
<paste raw documents — Kimi handles 128K well>

# Task (in order)
1. <step — explicit verb + object>
2. <step>
3. <step>

# Output Requirements
- Format: <markdown / JSON / table>
- Length: <bounded — e.g., ≤500 words>
- Sections (in this order):
  - <Section A>
  - <Section B>
  - <Section C>

# Constraints
- <requirement>
- <requirement>
- Do NOT: <forbidden behavior>

# Self-check before responding
- Did you cover all source documents?
- Did you follow the section order?
- Are length constraints met?
