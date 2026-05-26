#!/usr/bin/env python3
"""
run_golden.py — golden-case regression tests for the APEX 4D pipeline.

Loads cases from fixtures/golden_cases.json and runs each through the
deterministic D1+D2+D4 path. Checks that the output contains the expected
markers (role line, output_format spec, quality-check section).

This is not a strict equality test — D3 enrichment can produce variable text.
The check is "does the output contain the structural markers we expect?"

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
from apex_workflow import run_4d  # noqa: E402


FIXTURE_PATH = Path(__file__).parent / "fixtures" / "golden_cases.json"


def check_case(case: dict) -> tuple:
    """Run a case, return (passed, reason)."""
    rough = case["input"]
    platform = case.get("platform", "claude")
    result = run_4d(rough, platform=platform)

    for marker in case.get("must_contain", []):
        if marker not in result:
            return False, f"missing marker: {marker!r}"

    for marker in case.get("must_not_contain", []):
        if marker in result:
            return False, f"unexpected marker: {marker!r}"

    return True, "ok"


def main():
    if not FIXTURE_PATH.exists():
        print(f"FAIL: fixture file missing: {FIXTURE_PATH}")
        sys.exit(2)
    cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    passed = 0
    failed = []
    for i, case in enumerate(cases, 1):
        ok, reason = check_case(case)
        if ok:
            passed += 1
            print(f"  ✅ [{i:02d}] {case['name']}")
        else:
            failed.append((i, case["name"], reason))
            print(f"  ❌ [{i:02d}] {case['name']} — {reason}")

    print(f"\nGolden: {passed}/{len(cases)} passed")
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
