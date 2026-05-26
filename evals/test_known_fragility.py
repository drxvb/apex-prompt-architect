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
from apply_template import apply_template, apply_template_with_fixes
from validate_prompt import validate_prompt, detect_credentials
from apex_workflow import run_4d


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


# T7 — v1.0.1 regression: brace injection survives apply_template (T1.2)
# Without escaping, `{audience}` in user input would be silently substituted
# and `{0}` or `{evil}` would crash with KeyError / IndexError.
brace_inputs = [
    "summarize {audience} feedback",
    "render the {0} JSON for me",
    "use {evil} key please",
    "this is {literal} curly brace content",
]
for raw in brace_inputs:
    try:
        intent_braces = extract_intent(raw)
        out = apply_template(intent_braces, platform="claude")
        # The user's literal curly-brace text must appear in the output
        # (escaped braces in str.format() yield the original characters).
        if raw not in out:
            failed.append(("T7: brace passthrough", f"user text missing for {raw!r}"))
            print(f"  ❌ T7 ({raw!r}) — user text lost")
        else:
            passed += 1
            print(f"  ✅ T7 ({raw!r}): brace injection survives")
    except Exception as e:
        failed.append(("T7: brace crash", f"{raw!r} crashed: {e}"))
        print(f"  ❌ T7 ({raw!r}) — crashed: {e}")


# T8 — v1.0.1 regression: D2 fix_targets actually influence D3 output (T1.1)
intent_lean = extract_intent("write a poem")  # rough, will fail many D2 checks
# With no fix_targets, no injections
rendered_no_fixes, applied_no_fixes = apply_template_with_fixes(
    intent_lean, platform="claude", level="detailed", fix_targets=[]
)
# With explicit fix_targets, injections must appear
rendered_with_fixes, applied_with_fixes = apply_template_with_fixes(
    intent_lean, platform="claude", level="detailed",
    fix_targets=["examples", "safety", "audience_defined"]
)
if rendered_no_fixes == rendered_with_fixes:
    failed.append(("T8a: D2->D3 wiring", "fix_targets had no effect on output"))
    print("  ❌ T8a: D2->D3 wiring — fix_targets ignored")
else:
    passed += 1
    print("  ✅ T8a: D2->D3 wiring — fix_targets change rendered output")
if len(applied_with_fixes) < 3:
    failed.append(("T8b: applied_fixes count", f"expected >=3, got {len(applied_with_fixes)}"))
    print(f"  ❌ T8b: applied_fixes count — got {len(applied_with_fixes)}")
else:
    passed += 1
    print(f"  ✅ T8b: applied_fixes returns {len(applied_with_fixes)} injections")


# T9 — v1.0.1 regression: credential detection (T1.3)
cred_samples = [
    ("sk-ant-api03-AbCdEfGhIjKlMnOpQrStUvWxYz0123456", "OpenAI/Anthropic-style API key"),
    ("AKIAIOSFODNN7EXAMPLE", "AWS access key ID"),
    ("ghp_abcdefghij1234567890ABCDEFGHIJ1234567890", "GitHub personal access token"),
    ("Bearer abcdef1234567890ABCDEFGHIJK", "Bearer token"),
    ("-----BEGIN RSA PRIVATE KEY-----", "PEM private key"),
    ("password=hunter22supersecret", "embedded password/secret/api_key assignment"),
]
for sample, expected_label in cred_samples:
    detected = detect_credentials(f"please process this: {sample}")
    if expected_label in detected:
        passed += 1
        print(f"  ✅ T9 ({expected_label}): detected")
    else:
        failed.append(("T9: credential miss", f"{expected_label!r} not in {detected!r}"))
        print(f"  ❌ T9 ({expected_label}) — got {detected}")

# T9b — clean prompt has no false positives
clean_detected = detect_credentials("summarize this scientific paper for general readers")
if clean_detected:
    failed.append(("T9b: false positive", f"clean prompt flagged: {clean_detected!r}"))
    print(f"  ❌ T9b — false positive on clean prompt: {clean_detected}")
else:
    passed += 1
    print("  ✅ T9b: clean prompt produces no credential false positives")


# T10 — v1.0.1: workflow refuses on credentials before D1 runs
refuse_out = run_4d("optimize this: API_KEY=sk-ant-api03-AbCdEfGhIj1234567890AbCdEfGhIj")
if "Refusing to process" in refuse_out and "credential" in refuse_out.lower():
    passed += 1
    print("  ✅ T10: run_4d refuses when credential detected")
else:
    failed.append(("T10: workflow refusal", "run_4d did not refuse on credential input"))
    print("  ❌ T10: run_4d did not refuse on credential input")


# Summary
total = passed + len(failed)
print(f"\nFragility: {passed}/{total} passed")
sys.exit(0 if not failed else 1)
