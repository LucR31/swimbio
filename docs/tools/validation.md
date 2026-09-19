
We can change this later when you package it properly for PyPI.

---

# 9. Validation page

This one is particularly important.

```markdown
# Validation

Validation ensures that a `.swim` file follows the SWIM specification.

A validator can check:

- Required groups
- Required datasets
- Dataset dimensions
- Data types
- Units
- Metadata
- Format version
- Structural consistency

## Why validate?

A file can be technically readable as HDF5 while still being invalid as a SWIM file.

For example:

```text
HDF5 file
    ↓
Can HDF5 read it?
    ↓
        YES
         ↓
Does it follow SWIM?
         ↓
       MAYBE