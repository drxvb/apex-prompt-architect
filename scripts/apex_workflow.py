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

# Ensure utf-8 output on Windows (cp1252 default chokes on ✅ / ❌).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Import sibling modules.
sys.path.insert(0, str(Path(__file__).parent))
from extract_intent import extract_intent  # noqa: E402
from apply_template import apply_template_with_fixes  # noqa: E402
from validate_prompt import validate_prompt, format_checklist, detect_credentials  # noqa: E402


PLATFORMS = ("claude", "kimi", "minimax")


def _safe_read(path_str: str) -> str:
    """Read --input with a path-containment warning for absolute paths outside cwd.

    This isn't a sandbox — Python can still read any file the user can read —
    but it surfaces a warning when scripted/agentic callers pass surprising
    paths, e.g., `--input /etc/passwd` or `--input C:\\Windows\\System32\\...`.
    """
    p = Path(path_str).expanduser()
    try:
        p_resolved = p.resolve()
        cwd = Path.cwd().resolve()
        if p.is_absolute() and not str(p_resolved).startswith(str(cwd)):
            print(
                f"[apex_workflow] WARN: --input is an absolute path outside the "
                f"working directory: {p_resolved}",
                file=sys.stderr,
            )
    except OSError:
        pass
    return p.read_text(encoding="utf-8")


def _refuse_for_credentials(found: list) -> str:
    """Build the refusal artifact when credentials are detected in the rough prompt."""
    bullets = "\n".join(f"- {label}" for label in found)
    return (
        "# Refusing to process — credentials detected\n\n"
        "The rough prompt contains material matching the following "
        "credential-pattern(s):\n\n"
        f"{bullets}\n\n"
        "**What to do:** remove the credential value(s) from the rough prompt, "
        "or replace them with placeholders such as `<API_KEY>` or `${LLM_API_KEY}`. "
        "I deliberately do not echo the matched value here to avoid logging it.\n"
    )


def run_4d(rough_prompt: str, platform: str = "claude", mode: str = "standard") -> str:
    """Run the full 4D pipeline. Returns the formatted output."""
    # Pre-flight: refuse if credentials are present.
    creds = detect_credentials(rough_prompt)
    if creds:
        return _refuse_for_credentials(creds)

    # D1 — Deconstruct
    intent = extract_intent(rough_prompt)
    if intent.get("target_platform") in (None, "", "unspecified"):
        intent["target_platform"] = platform
    intent["_mode"] = mode

    # D2 — Diagnose
    checklist = validate_prompt(rough_prompt)
    fix_targets = [k for k, v in checklist.items() if v == "fail"]

    # D3 — Develop (D2 → D3 wired: fix_targets influence template injection)
    detailed, applied_fixes_detailed = apply_template_with_fixes(
        intent, platform=platform, level="detailed", fix_targets=fix_targets
    )
    compact, _ = apply_template_with_fixes(
        intent, platform=platform, level="compact", fix_targets=fix_targets
    )

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
    out.append("## D2 → D3 fixes applied")
    if applied_fixes_detailed:
        for fix in applied_fixes_detailed:
            out.append(f"- {fix}")
    elif fix_targets:
        out.append(
            "- (D2 found fix targets, but the deterministic D3 path can't "
            "auto-fix them on this platform/level; consider LLM enrichment)"
        )
        for ft in fix_targets:
            out.append(f"  - flagged: {ft}")
    else:
        out.append("- (no fix targets — rough prompt passed D2 cleanly)")
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

    rough = _safe_read(args.input)

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
