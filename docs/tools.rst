.. _tools:


Command Line Tools
==================

pyimagediet also comes with a command line tool `diet` which you can use to
compress files or generate configuration file tailored to your environment.


Generate configuration
----------------------

To find existing compression tools and print correct *commands* and
*pipelines* sections run:

        diet --check

This will print out configuration to standard output which you can save
as your configuration file (everything else needed should already be covered
by pyimagediet's default configuration).


Compress a files
----------------

You can compress files by running

        diet --config <path_to_config_file> <file>

where *path_to_config_file* points to configuration file and *file* is the
path of a file you want to compress.

Configuration file needs to have the same format as described in section
:ref:`configure` and can be either the output of the above described *check*
command or your customized version.
