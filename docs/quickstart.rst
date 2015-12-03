.. _quickstart:

Quick start
===========

To use pyimagediet it is enough to know just one function and how to construct
configuration object. To compress an image ``/tmp/big_picture.png`` with
configuration dict stored in ``config`` you would call:

::

        >>> from pyimagediet import diet
        >>> diet('/tmp/big_picture.png', config)
        True

Return value is the answer to "has the file been changed?". Configuration
dict is described in detail in section :ref:`configure`.
