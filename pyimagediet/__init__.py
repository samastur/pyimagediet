from .process import (
    DietException, NotFileDietException, ConfigurationErrorDietException,
    CompressFileDietException,
    read_yaml_configuration, parse_configuration, update_configuration,
    check_configuration, diet
)


__author__ = ("Marko Samastur <markos@gaivo.net>")

__version__ = "1.1.1"

__all__ = [
    DietException, NotFileDietException, ConfigurationErrorDietException,
    CompressFileDietException,
    read_yaml_configuration, parse_configuration, update_configuration,
    check_configuration, diet
]
