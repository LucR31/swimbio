Python
======

SWIM includes a Python implementation for reading, writing, and
validating SWIM files.


Requirements
------------

The current implementation uses Python together with HDF5-related
Python libraries.

See the project repository for the current installation requirements.


Development version
-------------------

The Python implementation is currently available in the SWIM
repository:

https://github.com/LucR31/swimbio


Reading a SWIM file
-------------------

A typical workflow is conceptually:

.. code-block:: python

   from swim_format import read_swim

   data = read_swim("race.swim")


Writing a SWIM file
-------------------

SWIM data can also be written using the Python implementation.


Validation
----------

Python tools can be used to validate SWIM files before distribution.

See :doc:`validation`.