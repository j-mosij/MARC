"""Deterministic MARC-Core and MARC-Disclosure validation."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .models import CoreRecord, DisclosureRecord

UNCERTAINTY_SOURCES = (
    "ambiguity",
    "missing_evidence",
    "capability_limit",
    "evidence_conflict",
    "safety",
)
REMEDIABILITIES = ("user_clarification", "retrieval", "tool", "human", "none")
SELECTED_ACTIONS = (
    "ANSWER",
    "CLARIFY",
    "RETRIEVE",
    "TOOL",
    "DELIBERATE",
    "ABSTAIN",
    "ESCALATE",
)
CONFIDENCE_BANDS = ("low", "medium", "high")
CONFIDENCE_TARGETS = (
    "answer",
    "direct_answer_suitability",
    "action_suitability",
)

CORE_REQUIRED = (
    "marc_version",
    "pre_capability",
    "uncertainty",
    "primary_source",
    "remediability",
    "selected_action",
    "confidence_band",
    "confidence_target",
    "recommended_next_step",
)
CORE_FIELDS = frozenset(
    CORE_REQUIRED
    + (
        "decision_id",
        "parent_decision_id",
        "iteration",
        "max_iterations",
        "calibration_profile",
        "secondary_source",
        "post_answer_confidence",
    )
)
DISCLOSURE_REQUIRED = (
    "answer",
    "confidence_band",
    "confidence_target",
    "uncertainty_source",
    "recommended_next_step",
)
DISCLOSURE_FIELDS = frozenset(DISCLOSURE_REQUIRED + ("selected_action",))

ACTION_REMEDIABILITY = {
    "CLARIFY": "user_clarification",
    "RETRIEVE": "retrieval",
    "TOOL": "tool",
    "ESCALATE": "human",
    "ABSTAIN": "none",
}


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """A validation outcome with hard errors separated from SHOULD warnings."""

    errors: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    @property
    def valid(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "errors": list(self.errors),
            "warnings": list(self.warnings),
        }


def _mapping(record: object) -> Mapping[str, Any] | None:
    if isinstance(record, (CoreRecord, DisclosureRecord)):
        return record.to_dict()
    if isinstance(record, Mapping):
        return record
    return None


def _is_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _validate_number(
    record: Mapping[str, Any], field: str, errors: list[str], *, nullable: bool = False
) -> None:
    if field not in record:
        return
    value = record[field]
    if value is None and nullable:
        return
    if not _is_number(value):
        errors.append(f"{field} must be a finite number")
    elif not 0.0 <= value <= 1.0:
        errors.append(f"{field} must be between 0.0 and 1.0")


def _validate_enum(
    record: Mapping[str, Any], field: str, values: tuple[str, ...], errors: list[str]
) -> None:
    if field in record and record[field] not in values:
        errors.append(f"{field} must be one of {', '.join(values)}")


def _validate_string(
    record: Mapping[str, Any],
    field: str,
    errors: list[str],
    *,
    maximum: int | None = None,
    nullable: bool = False,
) -> None:
    if field not in record:
        return
    value = record[field]
    if value is None and nullable:
        return
    if not isinstance(value, str):
        errors.append(f"{field} must be a string")
        return
    if not value:
        errors.append(f"{field} must not be empty")
    elif maximum is not None and len(value) > maximum:
        errors.append(f"{field} must be at most {maximum} characters")


def _validate_integer(record: Mapping[str, Any], field: str, errors: list[str]) -> None:
    if field not in record:
        return
    value = record[field]
    if not isinstance(value, int) or isinstance(value, bool):
        errors.append(f"{field} must be an integer")
    elif value < 0:
        errors.append(f"{field} must be greater than or equal to 0")


def _validate_unknown_fields(
    record: Mapping[str, Any], allowed: frozenset[str], errors: list[str]
) -> None:
    unknown = sorted(
        str(field)
        for field in record
        if field not in allowed and not str(field).startswith("x_")
    )
    for field in unknown:
        errors.append(f"unknown field: {field}")


def validate_core(record: object) -> ValidationResult:
    """Validate a MARC-Core record using draft-c4tz-marc-02 semantics."""

    data = _mapping(record)
    if data is None:
        return ValidationResult(errors=("record must be an object",))

    errors: list[str] = []
    warnings: list[str] = []

    for field in CORE_REQUIRED:
        if field not in data:
            errors.append(f"{field} is required")

    if "marc_version" in data and data["marc_version"] != "1.0":
        errors.append('marc_version must equal "1.0"')

    _validate_string(data, "decision_id", errors, maximum=128)
    _validate_string(data, "parent_decision_id", errors, maximum=128, nullable=True)
    _validate_integer(data, "iteration", errors)
    _validate_integer(data, "max_iterations", errors)
    _validate_string(data, "calibration_profile", errors, maximum=128)
    _validate_number(data, "pre_capability", errors)

    uncertainty = data.get("uncertainty")
    if "uncertainty" in data:
        if not isinstance(uncertainty, Mapping):
            errors.append("uncertainty must be an object")
        else:
            for source in UNCERTAINTY_SOURCES:
                qualified = f"uncertainty.{source}"
                if source not in uncertainty:
                    errors.append(f"{qualified} is required")
                else:
                    value = uncertainty[source]
                    if not _is_number(value):
                        errors.append(f"{qualified} must be a finite number")
                    elif not 0.0 <= value <= 1.0:
                        errors.append(f"{qualified} must be between 0.0 and 1.0")
            for field in sorted(str(key) for key in uncertainty if key not in UNCERTAINTY_SOURCES):
                errors.append(f"unknown uncertainty field: {field}")

    _validate_enum(data, "primary_source", UNCERTAINTY_SOURCES, errors)
    if "secondary_source" in data and data["secondary_source"] is not None:
        _validate_enum(data, "secondary_source", UNCERTAINTY_SOURCES, errors)
    _validate_enum(data, "remediability", REMEDIABILITIES, errors)
    _validate_enum(data, "selected_action", SELECTED_ACTIONS, errors)
    _validate_number(data, "post_answer_confidence", errors, nullable=True)
    _validate_enum(data, "confidence_band", CONFIDENCE_BANDS, errors)
    _validate_enum(data, "confidence_target", CONFIDENCE_TARGETS, errors)
    _validate_string(data, "recommended_next_step", errors, maximum=280)
    _validate_unknown_fields(data, CORE_FIELDS, errors)

    action = data.get("selected_action")
    if action == "ANSWER":
        if data.get("post_answer_confidence") is None:
            errors.append("post_answer_confidence must be non-null for ANSWER")
        if data.get("confidence_target") != "answer":
            errors.append('confidence_target must be "answer" for ANSWER')

    expected_remediability = ACTION_REMEDIABILITY.get(action)
    remediability = data.get("remediability")
    if (
        expected_remediability is not None
        and remediability in REMEDIABILITIES
        and remediability != expected_remediability
    ):
        warnings.append(
            f'remediability should be "{expected_remediability}" for {action}'
        )

    return ValidationResult(tuple(errors), tuple(warnings))


def validate_disclosure(record: object) -> ValidationResult:
    """Validate a MARC-Disclosure object using draft-c4tz-marc-02 semantics."""

    data = _mapping(record)
    if data is None:
        return ValidationResult(errors=("record must be an object",))

    errors: list[str] = []
    for field in DISCLOSURE_REQUIRED:
        if field not in data:
            errors.append(f"{field} is required")

    _validate_string(data, "answer", errors)
    _validate_enum(data, "confidence_band", CONFIDENCE_BANDS, errors)
    _validate_enum(data, "confidence_target", CONFIDENCE_TARGETS, errors)
    _validate_enum(data, "uncertainty_source", UNCERTAINTY_SOURCES, errors)
    _validate_string(data, "recommended_next_step", errors, maximum=280)
    _validate_enum(data, "selected_action", SELECTED_ACTIONS, errors)
    _validate_unknown_fields(data, DISCLOSURE_FIELDS, errors)
    return ValidationResult(tuple(errors))
