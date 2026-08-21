import json
from pathlib import Path

import pytest

from marc import project_disclosure, validate_disclosure

ROOT = Path(__file__).parents[1]


def load_answer() -> dict:
    return json.loads(
        (ROOT / "examples" / "valid" / "answer.json").read_text(encoding="utf-8")
    )


def test_projection_is_deterministic_and_omits_internal_scores() -> None:
    core = load_answer()
    disclosure = project_disclosure(core, "The documented behavior is supported.")
    assert disclosure == {
        "answer": "The documented behavior is supported.",
        "confidence_band": "high",
        "confidence_target": "answer",
        "uncertainty_source": "missing_evidence",
        "recommended_next_step": "review the cited sources",
        "selected_action": "ANSWER",
    }
    assert validate_disclosure(disclosure).valid
    assert "pre_capability" not in disclosure
    assert "post_answer_confidence" not in disclosure
    assert "uncertainty" not in disclosure


def test_projection_can_omit_optional_selected_action() -> None:
    disclosure = project_disclosure(
        load_answer(), "A concise answer.", include_selected_action=False
    )
    assert "selected_action" not in disclosure
    assert validate_disclosure(disclosure).valid


def test_projection_rejects_invalid_core() -> None:
    core = load_answer()
    core["primary_source"] = "none"
    with pytest.raises(ValueError, match="invalid MARC-Core record"):
        project_disclosure(core, "An answer")


def test_disclosure_requires_non_empty_user_visible_content() -> None:
    disclosure = project_disclosure(load_answer(), "An answer")
    disclosure["answer"] = ""
    result = validate_disclosure(disclosure)
    assert not result.valid
    assert result.errors == ("answer must not be empty",)
