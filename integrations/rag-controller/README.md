# RAG controller flow

This example demonstrates the MARC transition:

```text
missing_evidence -> RETRIEVE -> reassess -> ANSWER
```

The second record uses `parent_decision_id` to correlate the post-retrieval decision with the initial one. Retrieval mechanics are intentionally outside the example because MARC does not define a retrieval protocol.

```bash
python integrations/rag-controller/example.py
```
