# Generic agent flow

This executable example shows the controller boundary without depending on an agent framework:

```text
request -> assessment -> MARC-Core -> selected_action
        -> execution -> reassessment -> MARC-Disclosure
```

Run it after installing the Python package:

```bash
python integrations/generic-agent/example.py
```

The assessment values are deliberately supplied by the example controller. MARC defines their interoperable meaning, not the model-specific method used to compute them.
