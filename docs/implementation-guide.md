# Implementation guide

This guide explains how to consume the reference artifacts for `draft-c4tz-marc-02`. The Internet-Draft remains the source of MARC semantics.

## Emit MARC-Core

At every MARC decision point:

1. Set `marc_version` to `1.0`.
2. Estimate `pre_capability` before final-answer commitment.
3. include all five numeric uncertainty classes, each within `[0.0, 1.0]`;
4. choose one non-`none` `primary_source` and, optionally, a `secondary_source`;
5. choose the best available `remediability` and exactly one `selected_action`;
6. assign a coarse `confidence_band` and state its `confidence_target`;
7. include a concise, operational `recommended_next_step`;
8. for `ANSWER`, include a non-null `post_answer_confidence` and use confidence target `answer`.

Do not normalize the five uncertainty scores into a probability distribution. The scores are not mutually exclusive and need not sum to one.

The safety class is included in the uncertainty attribution object for operational convenience, but represents a control constraint rather than purely epistemic uncertainty. A controller must apply the governing safety, legal, or policy constraint when safety controls action selection.

## Errors and warnings

`validate_core` / `validateCore` enforce required fields, types, bounds, enums, extension names, and the ANSWER MUST rules as errors. These action/remediability expectations are warnings:

| Action | Normally expected remediability |
| --- | --- |
| `CLARIFY` | `user_clarification` |
| `RETRIEVE` | `retrieval` |
| `TOOL` | `tool` |
| `ESCALATE` | `human` |
| `ABSTAIN` | `none` |

A valid result can therefore contain warnings. Deployments that intentionally depart from a SHOULD relationship should document their local policy condition.

## Project disclosure

Call `project_disclosure(core, content)` in Python or `projectDisclosure(core, content)` in TypeScript only after the action has user-visible content. For non-terminal `RETRIEVE`, `TOOL`, or `DELIBERATE` decisions, a UI can defer disclosure until reassessment selects a terminal visible action.

The default projection includes `selected_action`. Pass `include_selected_action=False` in Python or `{ includeSelectedAction: false }` in TypeScript to omit it. Numeric scores are never projected by these functions.

## Deployment documentation

Structural validation cannot establish operational conformance. A deployment claiming conformance should document score normalization, confidence-band thresholds, task-specific calibration, loop bounds, private extensions, disclosure wording, carrier mappings, trust context, and policies affecting abstention or escalation.
