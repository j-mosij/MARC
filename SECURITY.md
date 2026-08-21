# Security policy

## Security model

MARC metadata can influence routing, tool use, abstention, escalation, audit decisions, downstream automation, and user reliance. Treat MARC-Core and MARC-Disclosure records as security-relevant metadata.

Implementations must separate untrusted user content from control metadata. A prompt, retrieved document, tool result, or downstream message must not be allowed to inject or overwrite `selected_action`, confidence rendering, or other MARC control fields without passing the controller and validator boundary.

JSON Schemas establish structure only. They do not provide authenticity, integrity, replay protection, request binding, emitter identity, authorization, or provenance. Cross-domain deployments must supply those protections through mechanisms outside MARC.

Operational deployments should also:

- bind records to the relevant request or session;
- authenticate emitters and integrity-protect carried metadata;
- constrain tool and retrieval permissions;
- bound `RETRIEVE`, `TOOL`, and `DELIBERATE` loops;
- minimize retention of sensitive decision metadata;
- validate a record before using it for routing or presentation.

## Reporting a vulnerability

Report vulnerabilities in this reference implementation privately through GitHub private vulnerability reporting: open the repository's **Security** tab and choose **Report a vulnerability** when that feature is enabled.

Do not include exploit details, affected user data, credentials, or other sensitive evidence in a public issue. If private vulnerability reporting is unavailable, open only a non-sensitive issue asking the maintainers to enable a private reporting channel; do not disclose the vulnerability in that issue.

Public issues using the Security concern template are appropriate for non-sensitive threat-model or hardening discussions only.

Reports should include the affected revision, component, impact, minimal reproduction conditions, and a suggested mitigation when available. The maintainers should acknowledge, triage, remediate, and coordinate disclosure based on impact; this repository does not promise a fixed response deadline.
