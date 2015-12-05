.. _configure:

Configuration
=============

As pyimagediet cannot guess which tools you want to use or how, you need to
provide that information to ``diet`` function. This configuration object has to
be a dict, but since dicts can be tedious to write, I prefer to start with
YAML representation and produce configuration dict with any of Python YAML
libraries.

Example configuration file:


.. literalinclude:: example.yml
    :language: yaml


Anatomy of a configuration object
---------------------------------

There are three sections that each configuration dict needs to have: *commands,
parameters and pipelines*.

*commands* contains another dict of label: path_to_executable pairs for each
command you may want to use. It does not matter if you also add commands that
are not used as long as those which are are also listed.

*parameters* section contains a dict of label: command_parameters pairs. Every
command from *commands* section has to have an entry here and they are matched
by their label which is also used in *pipelines* section.

pyimagediet is built on an assumption that each tool works on a file which is
passed to it using ``'{file}'`` variable. If the output is stored in a different
file, then that one should be marked with ``'{output_file}'``.

*pipelines* section describes which programs are executed and in what order for
matching file type. Its values are mime_type: list_of_apps. To match correctly
files correctly you need to provide only the second part of the file's MIME
type. For example JPEG images have a MIME type of *image/jpeg* so label has to
be *jpeg*. You can get correct MIME type by running:

::

        file --mime-type <file>

Each MIME type needs as value a list of tools to be used which are executed in
the same order as they are specified. You should use same labels as are used
in previously described sections and only those that you have installed on your
system.

It does not matter if you specify non-existing program in *commands* and
*parameters* section, but if you do it in pipeline then execution will fail
when that pipeline is invoked.

pyimagediet also comes with few default settings described in section
:ref:`defaults`. You only need to provide those values that are different which
will take precedence over defaults.


Optional parameters
~~~~~~~~~~~~~~~~~~~

While above parameters are all required to be there, there are also few
optional with which you can tweak pyimagediet behavior.

*backup* options takes as value file extension you want to attach to backups
of original file (without leading dot). If this option is not present, then
pyimagediet will not make backups and filename will now point to processed
version.

Internally it still creates a backup in case there was an error in which case
it will restore original version (so you should *always* end with non-corrupt
file), but that backup will be deleted afterwards unless told otherwise.

*keep_processed* should be set to true if you want to always keep the
processed version of the file. Otherwise pyimagediet will return whichever
version is smaller.
