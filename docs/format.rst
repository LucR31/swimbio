SWIM Format
===========

The SWIM format defines a standardized structure for storing swimming
race and biomechanical data in HDF5 files.


Format architecture
-------------------

At a high level, a SWIM dataset can contain:

.. code-block:: text

   SWIM
   ├── Athlete
   ├── Race
   ├── Results
   ├── Stroke metrics
   ├── Kinematics
   ├── IMU
   ├── Forces
   └── Video synchronization


Design principles
-----------------

The format is designed around several principles:

**Interoperability**

   Data should be usable across different software environments.

**Structured metadata**

   Measurements should be accompanied by the information required to
   interpret them.

**Extensibility**

   New measurement types should be possible without redesigning the
   entire format.

**Reproducibility**

   The dataset should preserve information necessary to understand the
   measurements and their provenance.


Underlying technology
---------------------

SWIM uses HDF5 as its storage layer.

HDF5 provides:

* Hierarchical data organization
* Numerical arrays
* Metadata attributes
* Compression
* Large dataset support
* Cross-platform libraries

SWIM defines the structure and semantics of the HDF5 content.


File extension
--------------

SWIM files use:

.. code-block:: text

   .swim

For example:

.. code-block:: text

   athlete_001_100m_freestyle.swim


Versioning
----------

Each SWIM file should identify the version of the SWIM specification
to which it conforms.

The current specification is:

**SWIM Format 1.0**