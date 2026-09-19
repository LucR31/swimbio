# Python

SWIM provides a Python implementation for reading, writing, and validating
`.swim` files.

## Requirements

The current implementation uses:

- Python
- NumPy
- h5py

## Development version

The Python implementation is currently available in the SWIM GitHub repository.

[View the Python implementation](https://github.com/LucR31/swimbio)

## Reading a file

Example:

```python
from swim_format import read_swim

data = read_swim("race.swim")