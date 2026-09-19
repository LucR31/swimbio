Examples
========

The SWIM repository contains example datasets demonstrating the
structure of SWIM files.


Example files
-------------

Example SWIM files are available in the project's ``examples/``
directory.

https://github.com/LucR31/swimbio/tree/main/examples


Example workflow
----------------

A typical example dataset may contain:

.. code-block:: text

   Athlete
      |
      +-- athlete_id
      +-- metadata
      |
      v
   Race
      |
      +-- event
      +-- distance
      +-- date
      |
      v
   Measurements
      |
      +-- stroke metrics
      +-- kinematics
      +-- IMU
      +-- forces


Purpose of the examples
-----------------------

The example files are intended to demonstrate how the format can be
used.

They do not necessarily represent the only valid way to collect or
organize swimming biomechanical data.