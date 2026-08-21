# Contributing

Contributions should improve implementability, validation, or independent interoperability for `draft-c4tz-marc-02`. This repository does not replace the Internet-Draft and must not silently introduce new MARC semantics.

We explicitly welcome:

- alternative MARC validators;
- agent framework integrations;
- gateway integrations;
- RAG integrations;
- interoperability test results;
- specification feedback.

Keep integrations small and vendor-neutral unless a real external project is reporting its own implementation. Classify normative MUST violations as errors and SHOULD deviations as warnings. If the draft is ambiguous, report the ambiguity instead of choosing a new normative rule in code.

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
npm ci
python -m pytest
npm test
npm run build
```

Before opening a pull request:

1. add or update common vectors for semantic behavior changes;
2. keep Python and TypeScript result ordering and messages equivalent;
3. validate every positive and negative example;
4. update documentation when a public API or mapping changes;
5. avoid claims of IETF endorsement, RFC status, or Internet Standard status.

## Independent implementations

If you implement MARC independently, please open an issue or pull
request containing:

- implementation language/framework;
- supported MARC profile;
- interoperability test results;
- deviations or ambiguities discovered.

Use the **Implementation report** issue template when possible. A result is useful even when some vectors fail: precise deviations help distinguish implementation defects from specification ambiguities.

## Specification feedback

Changes to MARC semantics belong in the Internet-Draft discussion. Repository issues may document an ambiguity and provide reproducible examples, but merged reference code should continue to identify the exact draft revision it implements.

## Security reports

Do not disclose suspected vulnerabilities in a public issue. Follow [SECURITY.md](SECURITY.md).
