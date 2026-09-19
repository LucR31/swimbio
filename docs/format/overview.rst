Format Overview
===============

This page provides a high-level overview of the SWIM data model.

The complete normative specification defines the exact structure,
datasets, attributes, data types, units, and conventions.


High-level structure
--------------------

A SWIM file is organized around several major components:

.. code-block:: text

   /athlete
   /race
   /results
   /stroke_metrics
   /kinematics
   /imu
   /forces
   /video


Optional components
-------------------

Not every SWIM file needs to contain every component.

For example, a dataset containing only race timing information may
contain athlete, race, and results data without any biomechanical
measurements.

A biomechanical experiment may additionally contain kinematics,
IMU, force, and video synchronization data.


Required versus optional data
-----------------------------

The specification distinguishes between required and optional
elements.

Implementations should not assume that every possible SWIM dataset
contains every measurement type.