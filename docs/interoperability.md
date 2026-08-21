# Interoperability

MARC interoperability means preserving field and action semantics even when implementations use different scoring, controller, storage, or transport internals.

## Test contract

[`../interoperability/vectors.json`](../interoperability/vectors.json) is the shared input. Each entry declares:

```json
{
  "name": "valid-answer",
  "record": {},
  "expected_valid": true,
  "expected_errors": [],
  "expected_warnings": []
}
```

The corpus covers every canonical action, invalid ANSWER confidence states, `primary_source: none`, an out-of-range score, an unknown enum value, and a SHOULD-level warning.

## Testing another implementation

1. Parse every record without preprocessing its values.
2. Produce a validity boolean plus separate error and warning lists.
3. Compare the result class against each vector.
4. Compare disclosure projection for the source fields described in the mapping guide.
5. Record the implementation version, language, passed vectors, and deviations.
6. Submit the result with the GitHub implementation-report template.

Exact validator message text is a repository-level regression contract, not a MARC protocol requirement. An independent implementation can use different wording while matching the expected validity and MUST/SHOULD classification; report message-only differences as such.

## Built-in agreement check

```bash
python -m pytest tests/test_interoperability.py
npm run test:interop
```

The TypeScript interoperability test evaluates the TypeScript validator, invokes the Python validator over the same vector file, and requires the two structured result sets to match exactly. CI fails on a disagreement.
