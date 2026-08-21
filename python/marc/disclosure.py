"""Projection from internal MARC-Core metadata to MARC-Disclosure."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .models import CoreRecord
from .validator import validate_core, validate_disclosure


def project_disclosure(
    core: Mapping[str, Any] | CoreRecord,
    answer: str,
    *,
    include_selected_action: bool = True,
) -> dict[str, Any]:
    """Deterministically project a valid core record and user-visible content.

    Internal numeric values are intentionally absent from the returned object.
    Set ``include_selected_action=False`` to omit the optional action label.
    """

    core_result = validate_core(core)
    if not core_result.valid:
        raise ValueError("invalid MARC-Core record: " + "; ".join(core_result.errors))

    data = core.to_dict() if isinstance(core, CoreRecord) else core
    disclosure: dict[str, Any] = {
        "answer": answer,
        "confidence_band": data["confidence_band"],
        "confidence_target": data["confidence_target"],
        "uncertainty_source": data["primary_source"],
        "recommended_next_step": data["recommended_next_step"],
    }
    if include_selected_action:
        disclosure["selected_action"] = data["selected_action"]

    disclosure_result = validate_disclosure(disclosure)
    if not disclosure_result.valid:
        raise ValueError(
            "invalid MARC-Disclosure projection: "
            + "; ".join(disclosure_result.errors)
        )
    return disclosure
