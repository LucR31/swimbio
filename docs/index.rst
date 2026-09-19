SWIM
====

Swimming Biomechanical Data Format

.. image:: https://img.shields.io/badge/format-SWIM%201.0-blue
   :alt: SWIM Format 1.0

.. image:: https://img.shields.io/badge/storage-HDF5-orange
   :alt: HDF5

.. image:: https://img.shields.io/github/license/LucR31/swimbio
   :alt: MIT License

**SWIM** is an open and extensible data format for storing swimming
athlete, race, and biomechanical data.

SWIM provides a common structure for combining data from race timing,
motion capture, video analysis, inertial measurement units, force
measurements, and other swimming-performance systems.

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   getting-started


Why SWIM?
---------

Swimming data are often collected using multiple systems, each using
different file formats, metadata structures, units, and conventions.

SWIM provides a common structure for bringing these data together in
a single ``.swim`` file.

.. code-block:: text

   Race timing ─────┐
   Video ───────────┤
   Motion capture ──┤
   IMU ─────────────┼──>  .swim  ──>  Analysis
   Force sensors ───┤
   Stroke analysis ─┘


What can a SWIM file contain?
-----------------------------

A SWIM file may contain:

* Athlete information
* Race information
* Race results and splits
* Stroke metrics
* Kinematic measurements
* IMU measurements
* Force measurements
* Video synchronization
* Experimental metadata

Not every SWIM file needs to contain every type of measurement.


Open and interoperable
----------------------

SWIM uses HDF5 as its underlying storage technology.

This means that SWIM files can be accessed using existing HDF5-compatible
software and libraries, including Python, MATLAB, R, Julia, C/C++, and
other environments.

HDF5 defines how the data are stored; SWIM defines the structure and
meaning of the data.


Current version
---------------

**SWIM Format 1.0**

The SWIM format specification is versioned independently from individual
software implementations.

.. note::

   This documentation describes SWIM Format 1.0.


Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: SWIM Format

   format
   format/overview
   format/athlete
   format/race
   format/biomechanics
   format/conventions


Tools
-----

.. toctree::
   :maxdepth: 2
   :caption: Tools and Implementations

   tools/python
   tools/matlab
   tools/validation


Data and Privacy
----------------

.. toctree::
   :maxdepth: 2
   :caption: Data Management

   privacy
   examples


Project
-------

.. toctree::
   :maxdepth: 1
   :caption: Project Information

   contributing
   changelog


Source code
-----------

The SWIM project is hosted on GitHub:

https://github.com/LucR31/swimbio

SWIM is released under the MIT License.