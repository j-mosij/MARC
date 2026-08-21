import json
from pathlib import Path

from marc import validate_core

ROOT = Path(__file__).parents[1]


def test_all_valid_examples_pass_without_warnings() -> None:
    paths = sorted((ROOT / "examples" / "valid").glob("*.json"))
    assert paths

    for path in paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        result = validate_core(record)
        assert result.valid, f"{path.name}: {result.errors}"
        assert result.warnings == (), f"{path.name}: {result.warnings}"


def test_uncertainty_scores_are_not_required_to_sum_to_one() -> None:
    record = json.loads(
        (ROOT / "examples" / "valid" / "clarify.json").read_text(encoding="utf-8")
    )
    assert sum(record["uncertainty"].values()) > 1.0
    assert validate_core(record).valid
