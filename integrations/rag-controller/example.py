"""Minimal RETRIEVE-to-ANSWER flow with decision correlation."""

from __future__ import annotations

import json
from typing import Any

from marc import project_disclosure, validate_core


def build_records() -> tuple[dict[str, Any], dict[str, Any]]:
    retrieve = {
        "marc_version": "1.0",
        "decision_id": "decision-001",
        "iteration": 0,
        "max_iterations": 2,
        "pre_capability": 0.45,
        "uncertainty": {
            "ambiguity": 0.05,
            "missing_evidence": 0.92,
            "capability_limit": 0.12,
            "evidence_conflict": 0.08,
            "safety": 0.0,
        },
        "primary_source": "missing_evidence",
        "remediability": "retrieval",
        "selected_action": "RETRIEVE",
        "confidence_band": "low",
        "confidence_target": "direct_answer_suitability",
        "recommended_next_step": "retrieve current authoritative evidence",
    }
    answer = {
        "marc_version": "1.0",
        "decision_id": "decision-002",
        "parent_decision_id": "decision-001",
        "iteration": 1,
        "max_iterations": 2,
        "pre_capability": 0.87,
        "uncertainty": {
            "ambiguity": 0.03,
            "missing_evidence": 0.18,
            "capability_limit": 0.08,
            "evidence_conflict": 0.05,
            "safety": 0.0,
        },
        "primary_source": "missing_evidence",
        "remediability": "none",
        "selected_action": "ANSWER",
        "post_answer_confidence": 0.89,
        "confidence_band": "high",
        "confidence_target": "answer",
        "recommended_next_step": "review the retrieved authority",
    }
    return retrieve, answer


if __name__ == "__main__":
    first, second = build_records()
    for record in (first, second):
        result = validate_core(record)
        if not result.valid:
            raise ValueError(result.errors)
    output = {
        "internal_decisions": [first, second],
        "disclosure": project_disclosure(
            second, "Retrieved authority supports the answer under the stated scope."
        ),
    }
    print(json.dumps(output, indent=2))
