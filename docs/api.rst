.. _api:

API
===

.. module:: pyimagediet

.. autofunction:: diet
.. autofunction:: parse_configuration

Calls to ``diet`` can be sped up by parsing configuration dict first with
``parse_configuration`` and then using its return value as ``diet`` ``config``
object.


Helpers
-------

.. autofunction:: check_configuration
.. autofunction:: update_configuration
.. autofunction:: read_yaml_configuration
