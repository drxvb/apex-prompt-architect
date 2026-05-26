#!/usr/bin/env python3
"""
compare_platforms.py — render the same intent across Claude / Kimi / MiniMax.

Wraps apex_workflow with platform=all and emits an additional comparison
table showing length, structure, and feature presence per platform.

Usage:
    python scripts/compare_platforms.py --input rough.md --output-dir ./out/
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from apex_workflow import run_4d  # noqa: E402

PLATFORMS = ("claude", "kimi", "minimax")


def render_table(rendered: dict) -> str:
    """Generate a markdown comparison table from rendered prompts."""
    rows = []
    rows.append("| Aspect | Claude | Kimi | MiniMax |")
    rows.append("|---|---|---|---|")
    rows.append(
        "| Approximate length | "
        + " | ".join(f"{len(rendered[p].split())} words" for p in PLATFORMS)
        + " |"
    )
    rows.append(
        "| Structure | "
        + " | ".join(("XML" if p == "claude" else "Markdown" if p == "kimi" else "Plain") for p in PLATFORMS)
        + " |"
    )
    rows.append(
        "| Verification block | "
        + " | ".join("Yes" if "verification" in rendered[p].lower() or "self-check" in rendered[p].lower() else "No" for p in PLATFORMS)
        + " |"
    )
    return "\n".join(rows)


def main():
    p = argparse.ArgumentParser(description="Compare APEX optimization across platforms")
    p.add_argument("--input", required=True)
    p.add_argument("--output-dir", default="./out")
    p.add_argument("--mode", default="standard", choices=("quick", "standard", "deep"))
    args = p.parse_args()

    rough = Path(args.input).read_text(encoding="utf-8")
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    rendered = {}
    for plat in PLATFORMS:
        result = run_4d(rough, platform=plat, mode=args.mode)
        rendered[plat] = result
        (out_dir / f"OUTPUT-{plat}.md").write_text(result, encoding="utf-8")

    # Write the comparison report
    report = ["# Multi-platform comparison", ""]
    report.append("## Differences at a glance")
    report.append(render_table(rendered))
    report.append("")
    report.append("## Variants")
    for plat in PLATFORMS:
        report.append(f"- See `OUTPUT-{plat}.md`")
    (out_dir / "COMPARISON.md").write_text("\n".join(report), encoding="utf-8")

    print(f"Wrote {out_dir}/OUTPUT-claude.md, OUTPUT-kimi.md, OUTPUT-minimax.md, COMPARISON.md")


if __name__ == "__main__":
    main()
