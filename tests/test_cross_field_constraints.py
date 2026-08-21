import copy
import json
from pathlib import Path

import pytest

from marc import validate_core

ROOT = Path(__file__).parents[1]


def load_example(name: str) -> dict:
    return json.loads(
        (ROOT / "examples" / "valid" / name).read_text(encoding="utf-8")
    )


def test_answer_requires_present_non_null_confidence() -> None:
    record = load_example("answer.json")
    del record["post_answer_confidence"]
    result = validate_core(record)
    assert not result.valid
    assert result.errors == ("post_answer_confidence must be non-null for ANSWER",)


def test_answer_requires_answer_confidence_target() -> None:
    record = load_example("answer.json")
    record["confidence_target"] = "direct_answer_suitability"
    result = validate_core(record)
    assert not result.valid
    assert result.errors == ('confidence_target must be "answer" for ANSWER',)


@pytest.mark.parametrize(
    "filename,wrong_remediability,warning",
    [
        ("clarify.json", "none", 'remediability should be "user_clarification" for CLARIFY'),
        ("retrieve.json", "none", 'remediability should be "retrieval" for RETRIEVE'),
        ("tool.json", "none", 'remediability should be "tool" for TOOL'),
        ("escalate.json", "none", 'remediability should be "human" for ESCALATE'),
        ("abstain.json", "human", 'remediability should be "none" for ABSTAIN'),
    ],
)
def test_should_mismatch_is_warning_not_error(
    filename: str, wrong_remediability: str, warning: str
) -> None:
    record = load_example(filename)
    record["remediability"] = wrong_remediability
    result = validate_core(record)
    assert result.valid
    assert result.errors == ()
    assert result.warnings == (warning,)


def test_private_extensions_are_accepted() -> None:
    record = load_example("answer.json")
    record["x_deployment_trace"] = {"opaque": True}
    assert validate_core(record).valid


def test_unknown_standard_field_is_rejected() -> None:
    record = copy.deepcopy(load_example("answer.json"))
    record["future_field"] = True
    result = validate_core(record)
    assert not result.valid
    assert "unknown field: future_field" in result.errors
