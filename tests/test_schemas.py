import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parents[1]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_schemas_are_valid_draft_2020_12() -> None:
    for path in sorted((ROOT / "schemas").glob("*.schema.json")):
        Draft202012Validator.check_schema(load_json(path))


def test_core_schema_accepts_positive_examples() -> None:
    validator = Draft202012Validator(
        load_json(ROOT / "schemas" / "marc-core.schema.json")
    )
    for path in sorted((ROOT / "examples" / "valid").glob("*.json")):
        errors = list(validator.iter_errors(load_json(path)))
        assert not errors, f"{path.name}: {[error.message for error in errors]}"


def test_core_schema_rejects_negative_examples() -> None:
    validator = Draft202012Validator(
        load_json(ROOT / "schemas" / "marc-core.schema.json")
    )
    for path in sorted((ROOT / "examples" / "invalid").glob("*.json")):
        assert not validator.is_valid(load_json(path)), path.name


def test_disclosure_schema_accepts_projected_shape() -> None:
    validator = Draft202012Validator(
        load_json(ROOT / "schemas" / "marc-disclosure.schema.json")
    )
    disclosure = {
        "answer": "The result is available.",
        "confidence_band": "high",
        "confidence_target": "answer",
        "uncertainty_source": "missing_evidence",
        "recommended_next_step": "review the supporting evidence",
        "selected_action": "ANSWER",
    }
    assert validator.is_valid(disclosure)
