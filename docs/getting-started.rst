Getting Started
================

This guide introduces the SWIM format and explains how to work with
``.swim`` files.


What is a SWIM file?
--------------------

A SWIM file is an HDF5 file that follows the SWIM data specification.

SWIM files use the ``.swim`` extension:

.. code-block:: text

   race_001.swim

The underlying HDF5 structure allows SWIM files to be inspected and
processed using standard HDF5 tools.


Basic workflow
--------------

A typical SWIM workflow is:

.. code-block:: text

   Collect data
        |
        v
   Process measurements
        |
        v
   Add metadata
        |
        v
   Create .swim file
        |
        v
   Validate
        |
        v
   Share / archive / analyse


Inspecting a SWIM file
----------------------

Because SWIM uses HDF5, files can be inspected using HDF5-compatible
software such as HDFView.

The SWIM specification defines the expected structure and meaning of
the data.


Python
------

A Python implementation is included in the SWIM repository.

See :doc:`tools/python` for information about the current implementation.


MATLAB
------

MATLAB support is also provided.

See :doc:`tools/matlab`.


Validation
----------

SWIM files should be validated before they are distributed or archived.

See :doc:`tools/validation`.