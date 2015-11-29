.. _install:

Installation
============

This part of the documentation covers the installation of pyimagediet.
The first step to using any software package is getting it properly installed.


Distribute & Pip
----------------

Installing pyimagediet is simple with `pip <https://pip.pypa.io>`_, just run
this in your terminal::

    $ pip install pyimagediet

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install pyimagediet

But, you really `shouldn't do that <https://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install>`_.


Get the Code
------------

pyimagediet is developed on GitHub, where the code is
`always available <https://github.com/samastur/pyimagediet>`_.

You can either clone the public repository::

    $ git clone git://github.com/samastur/pyimagediet.git

Download the `tarball <https://github.com/samastur/pyimagediet/tarball/master>`_::

    $ curl -OL https://github.com/samastur/pyimagediet/tarball/master

Or, download the `zipball <https://github.com/samastur/pyimagediet/zipball/master>`_::

    $ curl -OL https://github.com/samastur/pyimagediet/zipball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install


Installing "dependencies"
-------------------------

pyimagediet does not have a hard dependency on any external optimisation tool,
but it also does not do anything useful without any. You do need to install at
least one for each image format you want to handle.

You can find a list of some in :ref:`exttools`

