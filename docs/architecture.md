# Architecture

MARC is currently an individual Internet-Draft with Intended Status: Informational. This repository implements `draft-c4tz-marc-02`; it is not a separate specification.

## Processing model

```mermaid
flowchart LR
    R[Request] --> A[Assess capability]
    A --> U[Attribute uncertainty]
    U --> S[Select one action]
    S --> C[MARC-Core]
    C --> X[Execute or reassess]
    X --> P[Project user-visible content]
    P --> D[MARC-Disclosure]
```

At each decision point, a controller estimates pre-decision capability, scores every uncertainty class, selects exactly one primary source and action, identifies the confidence target, and emits MARC-Core. `RETRIEVE`, `TOOL`, and `DELIBERATE` return to assessment; implementations should bound those loops. A new `decision_id` and `parent_decision_id` can correlate the resulting records.

MARC-Disclosure is a lossy public projection. It retains content, the coarse confidence band and target, the primary uncertainty source, the recommended next step, and optionally the selected action. Numeric scores remain internal by default.

## Implementation boundaries

The reference implementation has four deliberately small layers:

1. JSON Schemas validate the JSON encoding and the ANSWER MUST constraints that JSON Schema can express.
2. Python and TypeScript validators implement deterministic structural errors and action/remediability warnings.
3. Projection functions enforce the MARC-Core-to-MARC-Disclosure mapping.
4. Common vectors verify that independent language implementations agree.

The validators do not select an action or infer scores. Those are controller responsibilities. The integrations demonstrate boundaries, not production orchestration systems.

## Extension handling

Fields beginning with `x_` are accepted as private extensions. Other unknown fields are rejected by the repository's strict validators and schemas. Receivers can adopt a different local policy for unknown fields, but extensions must not change required MARC field semantics.
