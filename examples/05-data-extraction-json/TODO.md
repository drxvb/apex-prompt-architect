# Example 05 — data extraction to JSON

**Status:** stub. Full worked example pending in v1.1.

## What this example should demonstrate
- D2 catches: no JSON schema, no handling of missing fields, no validation step
- D3 should add: explicit JSON schema with required/optional fields, "if field absent, use null" rule, schema-validation self-check, 2 few-shot examples (different input shapes → same schema)
- Three platforms show: all three benefit from few-shot here (extraction tasks are pattern-anchored); but Claude/Kimi can carry the schema as an embedded JSON Schema; MiniMax wants a worked example instead of a schema

## Pedagogical value
- Shows when few-shot examples are MANDATORY (extraction with non-trivial pattern)
- Shows JSON-schema as a constraint mechanism
