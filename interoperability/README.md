# MARC interoperability vectors

[`vectors.json`](vectors.json) is the language-neutral compatibility contract for this repository. Each vector contains a MARC-Core record and the exact validity, error, and warning outcome expected from an implementation of `draft-c4tz-marc-02`.

[`expected-results.json`](expected-results.json) is a compact canonical output set. It is intentionally redundant: tools can compare their generated results without first transforming the input vectors.

## Running the vectors

Python:

```bash
python -m pytest tests/test_interoperability.py
```

TypeScript and direct Python/TypeScript agreement check:

```bash
npm run test:interop
```

An independent implementation should preserve error/warning classification. Exact English message matching is required by this repository's vectors to make regressions deterministic, but MARC itself does not standardize validator wording.
