#!/usr/bin/env python3
"""
test_known_fragility.py — regression tests for known fragility classes.

Each test is a small, focused assertion against a known failure mode the
pipeline must handle correctly. Categories:

- T1: empty input handled gracefully
- T2: language detection (Arabic vs English) correct
- T3: target platform defaults to claude when unspecified
- T4: explicit platform mention overrides default
- T5: validate_prompt returns 12 entries
- T6: applying a template doesn't lose user-specified constraints

Python 3 stdlib only.
"""

import json
import sys
from pathlib import Path

# Ensure utf-8 output on Windows (cp1252 default chokes on ✅ / ❌).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from extract_intent import extract_intent
from apply_template import apply_template
from validate_prompt import validate_prompt


passed = 0
failed = []


def assert_eq(name, got, expected):
    global passed
    if got == expected:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed.append((name, f"expected {expected!r}, got {got!r}"))
        print(f"  ❌ {name} — expected {expected!r}, got {got!r}")


def assert_in(name, needle, haystack):
    global passed
    if needle in haystack:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed.append((name, f"missing {needle!r} in output"))
        print(f"  ❌ {name} — missing {needle!r}")


# T1 — empty input handled gracefully
try:
    intent = extract_intent("")
    assert intent["task_type"] == "generate"
    passed += 1
    print("  ✅ T1: empty input handled gracefully")
except Exception as e:
    failed.append(("T1", str(e)))
    print(f"  ❌ T1: {e}")

# T2 — language detection
intent_ar = extract_intent("لخِّص لي هذه الورقة العلميَّة")
assert_eq("T2a: Arabic detection", intent_ar["language"], "ar")
intent_en = extract_intent("Summarize this paper for me")
assert_eq("T2b: English detection", intent_en["language"], "en")

# T3 — default platform = claude
intent_default = extract_intent("write me a poem")
assert_eq("T3: target_platform default = claude", intent_default["target_platform"], "claude")

# T4 — explicit Kimi mention overrides
intent_kimi = extract_intent("write me a poem optimized for Kimi")
assert_eq("T4: explicit Kimi overrides default", intent_kimi["target_platform"], "kimi")

# T5 — validate_prompt returns 12 entries
results = validate_prompt("You are a helpful assistant.")
assert_eq("T5: 12 checklist entries", len(results), 12)

# T6 — apply_template fills role + task verbs
intent = extract_intent("summarize this paper for executives")
filled = apply_template(intent, platform="claude")
assert_in("T6a: filled template includes role marker", "You are", filled)
assert_in("T6b: filled template includes task verb", "Summarize", filled)


# Summary
total = passed + len(failed)
print(f"\nFragility: {passed}/{total} passed")
sys.exit(0 if not failed else 1)
