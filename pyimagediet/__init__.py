from  .process import (
    NotFileDietException, ConfigurationErrorDietException,
    CompressFileDietException,
    read_yaml_configuration, parse_configuration, update_configuration,
    check_configuration, diet
)


__author__ = ("Marko Samastur <markos@gaivo.net>")

__version__ = "1.0"

__all__ = [
    NotFileDietException, ConfigurationErrorDietException,
    CompressFileDietException,
    read_yaml_configuration, parse_configuration, update_configuration,
    check_configuration, diet
]
