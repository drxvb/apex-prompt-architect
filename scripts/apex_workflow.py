#!/usr/bin/env python3
"""
apex_workflow.py — CLI driver for the APEX 4D method.

Runs Deconstruct → Diagnose → Develop → Deliver against a rough prompt.
D1, D2, D4 are deterministic (no LLM). D3 enrichment is deterministic for
mechanical fixes; richer rewrites can be off-loaded to an LLM by configuring
LLM_API_URL / LLM_API_KEY / LLM_MODEL (see config.example.json).

Usage:
    python scripts/apex_workflow.py --input rough.md --output optimized.md
    python scripts/apex_workflow.py --input rough.md --platform kimi
    python scripts/apex_workflow.py --input rough.md --platform all --output-dir ./out/

Python 3 stdlib only. No pip install required.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# Import sibling modules.
sys.path.insert(0, str(Path(__file__).parent))
from extract_intent import extract_intent  # noqa: E402
from apply_template import apply_template  # noqa: E402
from validate_prompt import validate_prompt, format_checklist  # noqa: E402


PLATFORMS = ("claude", "kimi", "minimax")


def run_4d(rough_prompt: str, platform: str = "claude", mode: str = "standard") -> str:
    """Run the full 4D pipeline. Returns the formatted output."""
    # D1 — Deconstruct
    intent = extract_intent(rough_prompt)
    if intent.get("target_platform") in (None, "", "unspecified"):
        intent["target_platform"] = platform
    intent["_mode"] = mode

    # D2 — Diagnose
    checklist = validate_prompt(rough_prompt)
    fix_targets = [k for k, v in checklist.items() if v == "fail"]

    # D3 — Develop (mechanical fixes via template filling; LLM-enrichment optional)
    detailed = apply_template(intent, platform=platform, level="detailed", fix_targets=fix_targets)
    compact = apply_template(intent, platform=platform, level="compact", fix_targets=fix_targets)

    # D4 — Deliver
    out = []
    out.append(f"# Optimized Prompt — {intent.get('intent', 'untitled')}")
    out.append(f"**Target:** {platform} · **Mode:** {mode} · **Language:** {intent.get('language', 'en')}")
    out.append("")
    out.append("## Detailed prompt")
    out.append(detailed)
    out.append("")
    out.append("## Compact prompt")
    out.append(compact)
    out.append("")
    out.append("## Assumptions applied")
    for assumption in intent.get("_assumptions", []):
        out.append(f"- {assumption}")
    out.append("")
    out.append("## Quality check (12-point)")
    out.append(format_checklist(checklist))
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="APEX 4D prompt optimizer")
    p.add_argument("--input", required=True, help="Rough prompt file")
    p.add_argument("--output", help="Output file (single-platform mode)")
    p.add_argument("--output-dir", help="Output dir (--platform all mode)")
    p.add_argument("--platform", default="claude", choices=list(PLATFORMS) + ["all"])
    p.add_argument("--mode", default="standard", choices=("quick", "standard", "deep"))
    args = p.parse_args()

    rough = Path(args.input).read_text(encoding="utf-8")

    if args.platform == "all":
        out_dir = Path(args.output_dir or "./out")
        out_dir.mkdir(parents=True, exist_ok=True)
        for plat in PLATFORMS:
            result = run_4d(rough, platform=plat, mode=args.mode)
            (out_dir / f"OUTPUT-{plat}.md").write_text(result, encoding="utf-8")
            print(f"Wrote {out_dir / f'OUTPUT-{plat}.md'}")
    else:
        result = run_4d(rough, platform=args.platform, mode=args.mode)
        if args.output:
            Path(args.output).write_text(result, encoding="utf-8")
            print(f"Wrote {args.output}")
        else:
            print(result)


if __name__ == "__main__":
    main()
