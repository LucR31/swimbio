Athlete Data
============

SWIM provides a standardized location for athlete-related metadata.

Athlete identification and privacy should be considered when creating
or distributing SWIM datasets.


Athlete identifier
------------------

The ``athlete_id`` is the primary identifier for an athlete within a
dataset or study.

Identifiers should not contain directly identifying information.

For example:

.. code-block:: text

   athlete_id = "SWIM-8F31A2"

is preferable to:

.. code-block:: text

   athlete_id = "Jane_Smith"


Athlete names
-------------

Athlete names should be considered personally identifying information.

The athlete name should therefore be optional and should normally be
omitted from datasets intended for public distribution.


Pseudonymization
----------------

For research and public datasets, SWIM recommends using a pseudonymous
athlete identifier.

For example:

.. code-block:: text

   athlete_id: SWIM-8F31A2
   sex: F
   height_cm: 174
   weight_kg: 63

The mapping between the identifier and the athlete's real identity
should be stored separately from the SWIM dataset.


Identity key
------------

A research institution may maintain a separate identity key:

.. code-block:: text

   SWIM-8F31A2 -> Athlete A
   SWIM-91D7C4 -> Athlete B
   SWIM-44AC12 -> Athlete C

The identity key should not be included in a publicly distributed
SWIM dataset.

Access to the identity key should be appropriately restricted.


Important privacy note
----------------------

Removing an athlete's name does not necessarily make a dataset
anonymous.

A combination of demographic information, race information, timing,
biomechanical measurements, video, and other metadata may potentially
allow an individual to be identified.

Dataset publishers are responsible for assessing the privacy risks
associated with their particular dataset.


Privacy levels
--------------

SWIM datasets may be described as, for example:

* **Identified** -- direct identifying information is present.
* **Pseudonymized** -- direct identifiers have been replaced by
  pseudonymous identifiers, while a separate identity key exists.
* **De-identified** -- identifying information has been removed or
  transformed according to the applicable data-management procedure.

These descriptions do not constitute a legal determination of whether
a dataset is anonymous.