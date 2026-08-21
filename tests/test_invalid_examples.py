import json
from pathlib import Path

import pytest

from marc import validate_core

ROOT = Path(__file__).parents[1]

EXPECTED_ERROR = {
    "answer-null-confidence.json": "post_answer_confidence must be non-null for ANSWER",
    "answer-invalid-confidence-target.json": 'confidence_target must be "answer" for ANSWER',
    "invalid-primary-source-none.json": "primary_source must be one of ambiguity, missing_evidence, capability_limit, evidence_conflict, safety",
    "score-out-of-range.json": "uncertainty.missing_evidence must be between 0.0 and 1.0",
    "invalid-enumeration.json": "selected_action must be one of ANSWER, CLARIFY, RETRIEVE, TOOL, DELIBERATE, ABSTAIN, ESCALATE",
}


@pytest.mark.parametrize("filename,expected", EXPECTED_ERROR.items())
def test_invalid_example_fails(filename: str, expected: str) -> None:
    record = json.loads(
        (ROOT / "examples" / "invalid" / filename).read_text(encoding="utf-8")
    )
    result = validate_core(record)
    assert not result.valid
    assert expected in result.errors
