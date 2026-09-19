Human Participant Data and Privacy
==================================

SWIM can contain data originating from human participants.

Because swimming biomechanics may involve detailed personal,
performance, demographic, and video information, privacy should be
considered when creating and distributing SWIM datasets.


Direct identifiers
------------------

Direct identifiers such as:

* Name
* Email address
* Telephone number
* Home address
* Institutional identifiers

should generally not be included in datasets intended for public
distribution.


Pseudonymization
----------------

SWIM recommends using an opaque athlete identifier:

.. code-block:: text

   athlete_id: SWIM-8F31A2

The mapping between this identifier and the real identity should be
maintained separately and protected with appropriate access controls.


Encryption
----------

Encryption is not part of the SWIM file specification.

This is intentional.

SWIM defines the structure and semantics of the data. Encryption,
storage security, access control, and key management are deployment
and data-management concerns.

For example, a research institution may store:

.. code-block:: text

   Research storage
   |
   +-- public_data/
   |      |
   |      +-- race_001.swim
   |
   +-- restricted/
          |
          +-- identity_key.enc


Public versus controlled data
-----------------------------

Not every pseudonymized dataset is necessarily appropriate for public
release.

Datasets may contain combinations of information that could make an
individual identifiable.

Dataset publishers should therefore determine whether their data
should be:

* Publicly accessible
* Shared through controlled access
* Restricted to the research team


Responsibility
--------------

The SWIM format does not determine whether a particular dataset is
legally anonymous or suitable for public release.

The organization or researcher responsible for the dataset must
follow the applicable ethical, legal, institutional, and data
protection requirements.