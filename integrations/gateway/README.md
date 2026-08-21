# Gateway projection

This example separates internal control metadata from the downstream response:

- the gateway stores the complete MARC-Core record in an internal store;
- it returns a MARC-Disclosure object downstream;
- the projection excludes `pre_capability`, numeric uncertainty scores, and `post_answer_confidence`.

The in-memory dictionary represents a storage boundary, not a production database integration.

```bash
python integrations/gateway/example.py
```
