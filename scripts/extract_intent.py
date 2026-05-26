#!/usr/bin/env python3
"""
extract_intent.py — heuristic intent extraction (D1 of the APEX 4D method).

No LLM needed. Uses regex + keyword tables to extract task_type, audience,
domain, output_format, target_platform, language. Returns a dict with smart
defaults applied; assumptions are tracked in intent['_assumptions'].

Python 3 stdlib only.
"""

import re
from typing import Dict, List, Any


TASK_VERBS = {
    "summarize": ["summarize", "summary", "tldr", "tl;dr", "brief"],
    "extract": ["extract", "pull out", "identify"],
    "transform": ["rewrite", "transform", "convert", "translate"],
    "generate": ["generate", "create", "write", "produce", "compose"],
    "analyze": ["analyze", "analysis", "review", "audit", "evaluate"],
    "classify": ["classify", "categorize", "label", "tag"],
    "roleplay": ["pretend", "act as", "roleplay", "impersonate"],
    "plan": ["plan", "outline", "draft a roadmap", "design"],
}

AUDIENCE_HINTS = {
    "executive": ["executive", "exec", "ceo", "cto", "board", "leadership"],
    "developer": ["developer", "engineer", "programmer", "code"],
    "domain expert": ["expert", "specialist", "researcher", "academic"],
    "general technical": ["technical reader", "developer audience", "tech-aware"],
    "general": ["general audience", "anyone", "non-technical"],
}

FORMAT_HINTS = {
    "json": ["json", "structured", "schema"],
    "table": ["table", "tabular", "spreadsheet"],
    "markdown": ["markdown", "md", "doc"],
    "code": ["code", "function", "script"],
}

PLATFORM_HINTS = {
    "claude": ["claude", "anthropic"],
    "kimi": ["kimi", "moonshot"],
    "minimax": ["minimax", "mini-max"],
}

ARABIC_RANGE = re.compile(r"[؀-ۿ]")


def _detect_language(text: str) -> str:
    if ARABIC_RANGE.search(text):
        return "ar"
    return "en"


def _detect_one(text: str, table: Dict[str, List[str]]) -> str:
    """Lower-cased substring scan; returns first matching key or empty string."""
    low = text.lower()
    for key, keywords in table.items():
        for kw in keywords:
            if kw in low:
                return key
    return ""


def extract_intent(rough_prompt: str) -> Dict[str, Any]:
    """Run D1. Returns a structured intent dict with declared assumptions."""
    text = rough_prompt.strip()
    assumptions: List[str] = []

    # task_type
    task_type = _detect_one(text, TASK_VERBS)
    if not task_type:
        task_type = "generate"  # broadest fallback
        assumptions.append("task_type defaulted to 'generate' (no explicit task verb)")

    # audience
    audience = _detect_one(text, AUDIENCE_HINTS)
    if not audience:
        audience = "general technical reader"
        assumptions.append("audience defaulted to 'general technical reader'")

    # output_format
    output_format = _detect_one(text, FORMAT_HINTS)
    if not output_format:
        output_format = "markdown"
        assumptions.append("output_format defaulted to 'markdown'")

    # target_platform
    target_platform = _detect_one(text, PLATFORM_HINTS)
    if not target_platform:
        target_platform = "claude"
        assumptions.append("target_platform defaulted to 'claude'")

    # language
    language = _detect_language(text)

    # intent — best-effort one-sentence summary
    # Heuristic: take the first sentence up to 100 chars
    first_sentence = re.split(r"[.!?\n]", text)[0].strip()[:100] or text[:100]
    intent_summary = first_sentence if first_sentence else "improve a rough prompt"

    return {
        "intent": intent_summary,
        "task_type": task_type,
        "audience": audience,
        "domain": "unspecified",
        "constraints": [],
        "success_criteria": "implied",
        "output_format": output_format,
        "target_platform": target_platform,
        "language": language,
        "_assumptions": assumptions,
        "_rough_prompt": text,
    }


if __name__ == "__main__":
    import sys
    import json
    raw = sys.stdin.read() if not sys.argv[1:] else open(sys.argv[1], encoding="utf-8").read()
    print(json.dumps(extract_intent(raw), indent=2, ensure_ascii=False))
