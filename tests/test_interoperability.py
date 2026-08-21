import json
from pathlib import Path

from marc import validate_core

ROOT = Path(__file__).parents[1]


def test_python_matches_common_interoperability_vectors() -> None:
    vectors = json.loads(
        (ROOT / "interoperability" / "vectors.json").read_text(encoding="utf-8")
    )
    expected = json.loads(
        (ROOT / "interoperability" / "expected-results.json").read_text(
            encoding="utf-8"
        )
    )
    actual = []
    for vector in vectors:
        result = validate_core(vector["record"])
        assert result.valid is vector["expected_valid"], vector["name"]
        assert list(result.errors) == vector["expected_errors"], vector["name"]
        assert list(result.warnings) == vector["expected_warnings"], vector["name"]
        actual.append({"name": vector["name"], **result.as_dict()})
    assert actual == expected
