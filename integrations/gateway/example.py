"""Gateway boundary that stores core metadata and exposes disclosure only."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

from marc import project_disclosure, validate_core


class Gateway:
    def __init__(self) -> None:
        self._internal_records: dict[str, dict[str, Any]] = {}

    def emit(self, core: dict[str, Any], content: str) -> dict[str, Any]:
        result = validate_core(core)
        if not result.valid:
            raise ValueError(result.errors)
        decision_id = core.get("decision_id")
        if not isinstance(decision_id, str):
            raise ValueError("gateway storage requires decision_id")
        self._internal_records[decision_id] = deepcopy(core)
        return project_disclosure(core, content)

    def internal_record(self, decision_id: str) -> dict[str, Any]:
        return deepcopy(self._internal_records[decision_id])


if __name__ == "__main__":
    core_record = {
        "marc_version": "1.0",
        "decision_id": "gateway-001",
        "pre_capability": 0.88,
        "uncertainty": {
            "ambiguity": 0.03,
            "missing_evidence": 0.12,
            "capability_limit": 0.07,
            "evidence_conflict": 0.02,
            "safety": 0.0,
        },
        "primary_source": "missing_evidence",
        "remediability": "none",
        "selected_action": "ANSWER",
        "post_answer_confidence": 0.9,
        "confidence_band": "high",
        "confidence_target": "answer",
        "recommended_next_step": "review the cited source",
    }
    gateway = Gateway()
    downstream = gateway.emit(core_record, "The request was completed.")
    print(json.dumps({"downstream": downstream}, indent=2))
