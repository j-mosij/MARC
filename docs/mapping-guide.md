# Mapping guide

This guide maps `draft-c4tz-marc-02` semantics to the reference artifacts. It does not add MARC requirements.

## MARC-Core fields

| Field | JSON form | Mechanical checks |
| --- | --- | --- |
| `marc_version` | string | required, exactly `1.0` |
| `pre_capability` | number | required, `[0.0, 1.0]` |
| `uncertainty` | object | all five scores required and individually bounded |
| `primary_source` | enum | required; `none` rejected |
| `remediability` | enum | required |
| `selected_action` | enum | required, case-sensitive |
| `confidence_band` | enum | required: `low`, `medium`, or `high` |
| `confidence_target` | enum | required |
| `recommended_next_step` | string | required, 1–280 characters |
| identifiers and loop fields | string/integer | optional; string and non-negative constraints |
| `secondary_source` | enum or null | optional |
| `post_answer_confidence` | number or null | optional except non-null for `ANSWER`; bounded when numeric |

## Cross-field checks

| Condition | Result |
| --- | --- |
| `ANSWER` without non-null `post_answer_confidence` | error |
| `ANSWER` with target other than `answer` | error |
| action/remediability SHOULD mismatch | warning |

## Disclosure projection

| MARC-Disclosure | Source |
| --- | --- |
| `answer` | user-visible content associated with the selected action |
| `confidence_band` | `confidence_band` |
| `confidence_target` | `confidence_target` |
| `uncertainty_source` | `primary_source` |
| `recommended_next_step` | `recommended_next_step` |
| `selected_action` | `selected_action`, when exposed |

Numeric `pre_capability`, uncertainty scores, and `post_answer_confidence` are deliberately excluded from the default projection.

## Semantics that are not mechanically provable

Some draft requirements depend on behavior or deployment evidence rather than record shape:

- whether a score was actually computed before or after answer commitment;
- whether the chosen primary source is the most operationally relevant one;
- whether governing safety, legal, or policy constraints ran before other selection logic;
- whether confidence-band thresholds are calibrated, monotonic, non-overlapping, and documented;
- whether retrieval, tool use, or deliberation has effective cost, time, or iteration bounds;
- whether a recommended next step is genuinely concise and operational rather than merely a non-empty string;
- whether identity, integrity, replay, binding, and provenance controls are effective;
- whether the visible disclosure creates misuse, overreliance, or human-factors risk.

Schemas and validators can check declarations about these properties, but cannot prove the underlying controller behavior. Implementers need tests, calibration evidence, policy review, and carrier-layer controls outside MARC.
