# Trust model

MARC is currently an individual Internet-Draft with Intended Status: Informational.

> A MARC record is an assertion about a decision point. It is not proof that the selected action, confidence band, uncertainty source, confidence target, or answer is correct.

A receiver must evaluate the relationship under which the record was produced. MARC identifies four useful trust contexts:

| Context | Meaning |
| --- | --- |
| `local` | The record is generated and consumed within one administrative domain. |
| `delegated` | A component generates the record under the receiver's operational policy. |
| `cross-domain` | The record arrives from another administrative domain. |
| `attested` | External mechanisms bind the record to an authenticated emitter, request context, integrity-protected metadata, or equivalent provenance. |

Cross-domain deployments need mechanisms outside MARC for authentication, integrity, replay protection, request binding, and provenance. MARC itself does not implement these mechanisms. They belong to the carrier protocol or deployment environment.

Schema validity establishes only that a record has the expected JSON shape and mechanically testable relationships. It does not establish that scores are calibrated, a source attribution is honest, a policy was followed, or an answer is correct. Apply ordinary authorization, validation, provenance, and safety controls to downstream actions.
