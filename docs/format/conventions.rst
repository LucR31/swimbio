Units and Conventions
=====================

SWIM uses explicit units and conventions to make datasets
interoperable.


Units
-----

Measurements should use SI units unless otherwise specified by the
SWIM specification.

Examples include:

.. list-table::
   :header-rows: 1

   * - Quantity
     - Unit
   * - Time
     - seconds (s)
   * - Distance
     - metres (m)
   * - Velocity
     - metres per second (m/s)
   * - Acceleration
     - metres per second squared (m/s²)
   * - Force
     - newtons (N)


Coordinate systems
------------------

Coordinate systems must be explicitly defined where relevant.

This is particularly important for:

* Motion capture
* IMUs
* Force measurements
* Video-based measurements


Sampling
--------

Time-series measurements should include sufficient information to
determine their temporal sampling.

This may include:

* Sampling frequency
* Timestamps
* Start time
* Synchronization information


Missing data
------------

Missing or unavailable measurements should follow the conventions
defined by the SWIM specification.

Implementations should not silently interpret missing values as zero.