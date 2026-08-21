"""Typed data models for the MARC 1.0 JSON encoding."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal, TypeAlias

UncertaintySource: TypeAlias = Literal[
    "ambiguity",
    "missing_evidence",
    "capability_limit",
    "evidence_conflict",
    "safety",
]
Remediability: TypeAlias = Literal[
    "user_clarification", "retrieval", "tool", "human", "none"
]
SelectedAction: TypeAlias = Literal[
    "ANSWER", "CLARIFY", "RETRIEVE", "TOOL", "DELIBERATE", "ABSTAIN", "ESCALATE"
]
ConfidenceBand: TypeAlias = Literal["low", "medium", "high"]
ConfidenceTarget: TypeAlias = Literal[
    "answer", "direct_answer_suitability", "action_suitability"
]


@dataclass(frozen=True, slots=True)
class Uncertainty:
    """Class-specific scores; values are salience estimates, not probabilities."""

    ambiguity: float
    missing_evidence: float
    capability_limit: float
    evidence_conflict: float
    safety: float


@dataclass(frozen=True, slots=True)
class CoreRecord:
    """Typed representation of a MARC-Core record."""

    marc_version: str
    pre_capability: float
    uncertainty: Uncertainty
    primary_source: UncertaintySource
    remediability: Remediability
    selected_action: SelectedAction
    confidence_band: ConfidenceBand
    confidence_target: ConfidenceTarget
    recommended_next_step: str
    decision_id: str | None = None
    parent_decision_id: str | None = None
    iteration: int | None = None
    max_iterations: int | None = None
    calibration_profile: str | None = None
    secondary_source: UncertaintySource | None = None
    post_answer_confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return the JSON-compatible representation, omitting null optionals."""

        return {key: value for key, value in asdict(self).items() if value is not None}


@dataclass(frozen=True, slots=True)
class DisclosureRecord:
    """Typed representation of a MARC-Disclosure object."""

    answer: str
    confidence_band: ConfidenceBand
    confidence_target: ConfidenceTarget
    uncertainty_source: UncertaintySource
    recommended_next_step: str
    selected_action: SelectedAction | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return the JSON-compatible representation, omitting null optionals."""

        return {key: value for key, value in asdict(self).items() if value is not None}
