Validation
==========

Validation determines whether a file follows the SWIM specification.


Why validate?
-------------

A file can be a valid HDF5 file without being a valid SWIM file.

For example:

.. code-block:: text

   HDF5 file
       |
       +-- Is the file readable as HDF5?
       |          |
       |          +-- YES
       |
       +-- Does it follow the SWIM specification?
                  |
                  +-- YES / NO


Validation checks
-----------------

A SWIM validator may check:

* Format version
* Required groups
* Required datasets
* Dataset dimensions
* Data types
* Units
* Metadata
* Structural consistency


Recommended workflow
--------------------

.. code-block:: text

   Create .swim
        |
        v
     Validate
        |
        +---- errors ----> Fix
        |                   |
        |                   v
        +-------------- Validate
                            |
                            v
                       Share / archive