#!/usr/bin/env python3
"""
apply_template.py — fill a per-platform template with a structured intent.

Reads templates/for-<platform>.md and produces a filled prompt. The fill is
deterministic and uses only the intent dict; LLM enrichment is an optional
follow-up step not implemented in this starter.

D2->D3 wiring (v1.0.1): `fix_targets` from D2 now influences D3 output —
when specific checks failed, this module injects placeholder blocks marked
as TODO so the human downstream sees exactly what D2 flagged that the
deterministic template can't fully fix on its own.

Python 3 stdlib only.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple


REPO_ROOT = Path(__file__).parent.parent


# Detailed wrappers, per platform. Compact wrappers are tighter.

DETAILED = {
    "claude": """<role>
You are a {audience}-facing specialist. Your task is to {task_verb} the provided input with attention to {domain} conventions.
</role>

<context>
{rough_prompt}
</context>

<instructions>
1. Read the input carefully.
2. {task_verb_imperative} the input following the format below.
3. Cite the source by section when claims are drawn from it.

Before answering, think step-by-step about the most likely failure mode for this task.
</instructions>

<constraints>
- Preserve the user's original constraints.
- Do NOT add information not in the source.
- Tone: professional, clear, concise.
</constraints>

<output_format>
Use markdown with explicit section headers. Format: {output_format}.
</output_format>

<verification>
Before responding, confirm:
1. Every claim traces to a specific section of the input.
2. The output format matches the requested shape.
3. You have not added domain knowledge from outside the input.
</verification>""",

    "kimi": """# Role
You are a {audience}-facing specialist. Mission: {task_verb} the provided input.

# Source Material
{rough_prompt}

# Task (in order)
1. Read every section before writing.
2. {task_verb_imperative} the input following the format below.
3. Cite sections when drawing claims from them.

# Output Requirements
- Format: {output_format}
- Tone: professional, clear, concise
- Preserve original constraints

# Constraints
- Do not add information not in the source.
- Cite sections by name when relevant.

# Self-check before responding
- Did you cover all source material?
- Does the output follow the requested format?
- Is the response free of added domain knowledge?""",

    "minimax": """You are a {audience}-facing specialist. Your task: {task_verb} the input.

Input: {rough_prompt}

Produce a {output_format} response. Preserve original constraints. Do not add information not in the source. Tone: professional, clear, concise.""",
}

COMPACT = {
    "claude": "You are a {audience} specialist. {task_verb_imperative} the input as {output_format}. Preserve constraints; do not add external info; cite sections when relevant.",
    "kimi": "Role: {audience} specialist. Task: {task_verb} the input -> {output_format}. Constraints: preserve user constraints; no external info; cite sources.",
    "minimax": "{task_verb_imperative} this {output_format}: preserve constraints, no external info, cite sources.",
}


def _imperative(task_verb: str) -> str:
    """Return imperative form of the task verb."""
    mapping = {
        "summarize": "Summarize",
        "extract": "Extract from",
        "transform": "Transform",
        "generate": "Generate",
        "analyze": "Analyze",
        "classify": "Classify",
        "roleplay": "Roleplay as",
        "plan": "Plan",
    }
    return mapping.get(task_verb, task_verb.title())


def _inject_fix_target_blocks(rendered: str, platform: str, level: str,
                              fix_targets: List[str]) -> Tuple[str, List[str]]:
    """Inject placeholder blocks for D2 failures the static template can't fix.

    Returns (rendered_with_injections, list_of_applied_fixes).
    Only fires for `detailed` Claude prompts — compact and other platforms
    use the failures purely as advisory.
    """
    applied: List[str] = []
    if level != "detailed" or platform != "claude":
        return rendered, applied

    injections: List[str] = []
    if "examples" in fix_targets and "<examples>" not in rendered:
        injections.append(
            "\n<examples>\n<!-- D2 flagged this prompt as needing few-shot "
            "examples. Insert 1-3 input/output pairs in the user's domain. -->\n"
            "</examples>"
        )
        applied.append("examples -> empty <examples> block injected as a TODO")

    if "audience_defined" in fix_targets:
        injections.append(
            "\n<!-- D2: no explicit audience marker detected in rough input. "
            "Refine the role line above with a concrete audience descriptor. -->"
        )
        applied.append("audience_defined -> reminder comment injected")

    if "safety" in fix_targets:
        injections.append(
            "\n<safety>\n<!-- D2 flagged this prompt as needing safety/compliance "
            "language. Add domain-appropriate clauses (e.g., 'do not store PII', "
            "'this is informational, not professional advice'). -->\n</safety>"
        )
        applied.append("safety -> empty <safety> block injected as a TODO")

    if injections:
        rendered = rendered + "\n" + "\n".join(injections)
    return rendered, applied


def apply_template(intent: Dict[str, Any], platform: str = "claude", level: str = "detailed",
                   fix_targets: List[str] = None) -> str:
    """Fill the platform/level template using fields from the intent dict.

    Backwards-compatible: returns a string (the rendered prompt). Callers that
    need the list of applied fixes should use `apply_template_with_fixes`.
    """
    rendered, _ = apply_template_with_fixes(intent, platform, level, fix_targets)
    return rendered


def apply_template_with_fixes(intent: Dict[str, Any], platform: str = "claude",
                              level: str = "detailed",
                              fix_targets: List[str] = None) -> Tuple[str, List[str]]:
    """Like apply_template, but also returns the list of fix injections applied.

    This is the wiring D2 -> D3 promises in SKILL.md. Use this from apex_workflow
    so users see WHAT D2 found and HOW D3 surfaced it.
    """
    fix_targets = fix_targets or []
    templates = DETAILED if level == "detailed" else COMPACT
    template = templates.get(platform, templates["claude"])

    rough = intent.get("_rough_prompt", "<user input here>")

    domain = intent.get("domain") or "the relevant"
    if domain == "unspecified":
        domain = "the relevant"

    # Note: str.format() substitutes value strings verbatim — it does NOT
    # re-scan them for placeholders. So braces in `rough` (e.g. user pastes
    # "summarize {audience} feedback") are safe by Python's semantics; no
    # escaping needed. The T7 fragility test enforces this contract so
    # future refactors don't accidentally introduce escape logic that
    # would double-up the user's braces.
    rendered = template.format(
        audience=intent.get("audience", "general technical reader"),
        task_verb=intent.get("task_type", "process"),
        task_verb_imperative=_imperative(intent.get("task_type", "process")),
        domain=domain,
        output_format=intent.get("output_format", "markdown"),
        rough_prompt=rough,
    )

    rendered, applied = _inject_fix_target_blocks(rendered, platform, level, fix_targets)
    return rendered, applied


if __name__ == "__main__":
    import sys
    import json
    intent = json.loads(sys.stdin.read())
    platform = sys.argv[1] if len(sys.argv) > 1 else "claude"
    level = sys.argv[2] if len(sys.argv) > 2 else "detailed"
    print(apply_template(intent, platform=platform, level=level))
