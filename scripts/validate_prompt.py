#!/usr/bin/env python3
"""
validate_prompt.py — 12-point quality-checklist linter.

Scans a prompt and returns a dict {check_name: pass | warn | fail}. Can be
run standalone against any prompt file, or imported by apex_workflow.py
during D2.

Python 3 stdlib only. Heuristic checks — false positives possible.

Usage:
    python scripts/validate_prompt.py --input existing.md
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Ensure utf-8 output on Windows (cp1252 default chokes on ✅ / ❌).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


# Credential patterns — used by detect_credentials() to enforce the
# "refuse processing on credentials" safety rule from references/07.
# Each entry: (pattern, human-readable label).
CREDENTIAL_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"sk-(ant-)?[A-Za-z0-9_-]{20,}"), "OpenAI/Anthropic-style API key"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key ID"),
    (re.compile(r"\bASIA[0-9A-Z]{16}\b"), "AWS temporary access key"),
    (re.compile(r"ghp_[A-Za-z0-9]{30,}"), "GitHub personal access token"),
    (re.compile(r"gho_[A-Za-z0-9]{30,}"), "GitHub OAuth token"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{60,}"), "GitHub fine-grained PAT"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{20,}"), "Bearer token"),
    (re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "JWT"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "PEM private key"),
    (re.compile(r"(?i)(?:password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"]?[^\s'\"]{6,}"),
     "embedded password/secret/api_key assignment"),
]


def detect_credentials(text: str) -> List[str]:
    """Return a list of human-readable labels for credential patterns found in text.

    Empty list means clean. Used by apex_workflow.py to gate the 4D pipeline:
    if credentials are detected, the workflow refuses and tells the user
    what to remove — without echoing the credential value itself.
    """
    found: List[str] = []
    for pattern, label in CREDENTIAL_PATTERNS:
        if pattern.search(text):
            found.append(label)
    return found


# Heuristic markers — each check returns pass / warn / fail.

ROLE_MARKERS = re.compile(r"\b(you are|act as|role[: ]|<role>)\b", re.I)
TASK_VERBS = ["summarize", "extract", "classify", "compare", "generate", "transform",
              "analyze", "review", "identify", "rewrite", "refactor", "translate", "plan"]
AUDIENCE_MARKERS = ["audience", "reader", "for a", "developer", "exec", "expert"]
CONTEXT_BOUNDARY = re.compile(r"\b(focus on|do not address|exclude|scope|out of scope)\b", re.I)
FORMAT_MARKERS = re.compile(r"\b(json|markdown|format|template|schema|table)\b", re.I)
CONSTRAINT_MARKERS = re.compile(r"\b(must|do not|never|always|≤|<=|maximum|minimum|words)\b", re.I)
EXAMPLE_MARKERS = re.compile(r"\b(example|for instance|e\.g\.|input:.*output:)\b", re.I | re.S)
FAILURE_MARKERS = re.compile(r"\b(if .* (unclear|missing|absent|unavailable))\b", re.I)
VERIFICATION_MARKERS = re.compile(r"\b(before (answering|responding)|self.?check|confirm|verify)\b", re.I)
TONE_MARKERS = re.compile(r"\b(tone|formal|casual|professional|direct|concise)\b", re.I)
SAFETY_MARKERS = re.compile(r"\b(do not (generate|expose|store)|never share|refuse|sensitive)\b", re.I)


def _check_role(text: str) -> str:
    if not ROLE_MARKERS.search(text):
        return "fail"
    # warn if just "helpful assistant"
    if re.search(r"helpful assistant", text, re.I):
        return "warn"
    return "pass"


def _check_task_verb(text: str) -> str:
    return "pass" if any(v in text.lower() for v in TASK_VERBS) else "fail"


def _check_audience(text: str) -> str:
    return "pass" if any(a in text.lower() for a in AUDIENCE_MARKERS) else "fail"


def _check_context_boundary(text: str) -> str:
    return "pass" if CONTEXT_BOUNDARY.search(text) else "warn"


def _check_output_format(text: str) -> str:
    return "pass" if FORMAT_MARKERS.search(text) else "fail"


def _check_constraints(text: str) -> str:
    return "pass" if CONSTRAINT_MARKERS.search(text) else "fail"


def _check_examples(text: str) -> str:
    # Examples are conditional. Return warn if missing (might or might not need them).
    return "pass" if EXAMPLE_MARKERS.search(text) else "warn"


def _check_failure_modes(text: str) -> str:
    return "pass" if FAILURE_MARKERS.search(text) else "fail"


def _check_verification(text: str) -> str:
    return "pass" if VERIFICATION_MARKERS.search(text) else "warn"


def _check_length(text: str) -> str:
    # Heuristic: warn if prompt is very short (< 50 words) or very long (> 1500 words).
    words = len(text.split())
    if words < 50:
        return "warn"
    if words > 1500:
        return "warn"
    return "pass"


def _check_tone(text: str) -> str:
    return "pass" if TONE_MARKERS.search(text) else "warn"


def _check_safety(text: str) -> str:
    # Safety is conditional on domain. Just return warn so the user can confirm domain.
    return "pass" if SAFETY_MARKERS.search(text) else "warn"


CHECKS = [
    ("role_assigned", _check_role),
    ("task_verb_explicit", _check_task_verb),
    ("audience_defined", _check_audience),
    ("context_boundaries", _check_context_boundary),
    ("output_format", _check_output_format),
    ("constraints", _check_constraints),
    ("examples", _check_examples),
    ("failure_modes", _check_failure_modes),
    ("verification", _check_verification),
    ("platform_length", _check_length),
    ("tone", _check_tone),
    ("safety", _check_safety),
]


def validate_prompt(text: str) -> Dict[str, str]:
    """Run all 12 checks. Returns a dict of {check_name: pass | warn | fail}."""
    return {name: fn(text) for name, fn in CHECKS}


def format_checklist(results: Dict[str, str]) -> str:
    """Format the results dict for the Quality check section of the output."""
    icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}
    lines = []
    for name, status in results.items():
        pretty = name.replace("_", " ").capitalize()
        lines.append(f"- {icon[status]} {pretty}")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="12-point prompt-quality linter")
    p.add_argument("--input", required=True, help="Prompt file to validate")
    args = p.parse_args()
    text = Path(args.input).read_text(encoding="utf-8")
    results = validate_prompt(text)
    print(format_checklist(results))
    fails = sum(1 for v in results.values() if v == "fail")
    exit(1 if fails > 0 else 0)


if __name__ == "__main__":
    main()
