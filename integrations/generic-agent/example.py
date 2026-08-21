"""Minimal, vendor-neutral MARC decision flow."""

from __future__ import annotations

import json
from typing import Any

from marc import project_disclosure, validate_core


def assess(request: str) -> dict[str, Any]:
    """Return an illustrative controller assessment for one request."""

    is_ambiguous = "region" not in request.lower()
    if is_ambiguous:
        return {
            "marc_version": "1.0",
            "decision_id": "generic-001",
            "pre_capability": 0.4,
            "uncertainty": {
                "ambiguity": 0.9,
                "missing_evidence": 0.2,
                "capability_limit": 0.1,
                "evidence_conflict": 0.0,
                "safety": 0.0,
            },
            "primary_source": "ambiguity",
            "remediability": "user_clarification",
            "selected_action": "CLARIFY",
            "confidence_band": "low",
            "confidence_target": "direct_answer_suitability",
            "recommended_next_step": "ask which region applies",
        }
    return {
        "marc_version": "1.0",
        "decision_id": "generic-001",
        "pre_capability": 0.85,
        "uncertainty": {
            "ambiguity": 0.05,
            "missing_evidence": 0.1,
            "capability_limit": 0.08,
            "evidence_conflict": 0.02,
            "safety": 0.0,
        },
        "primary_source": "missing_evidence",
        "remediability": "none",
        "selected_action": "ANSWER",
        "post_answer_confidence": 0.87,
        "confidence_band": "high",
        "confidence_target": "answer",
        "recommended_next_step": "review the answer against local requirements",
    }


def run(request: str) -> dict[str, Any]:
    core = assess(request)
    result = validate_core(core)
    if not result.valid:
        raise ValueError(result.errors)
    visible_content = (
        "Which region should I use?"
        if core["selected_action"] == "CLARIFY"
        else "The request can be answered under the stated regional context."
    )
    return project_disclosure(core, visible_content)


if __name__ == "__main__":
    print(json.dumps(run("Summarize the applicable requirements"), indent=2))
