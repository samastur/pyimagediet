import copy
import filecmp
import magic
from os.path import exists
import shutil
import yaml


class DietException(Exception):
    pass


def read_yaml_configuration(filename):
    '''Parse configuration in YAML format into a Python dict'''
    with open(filename, 'r') as f:
        config = yaml.load(f.read())
    return config


def determinetype(filename):
    '''Determine the file type and return it.'''
    ftype = magic.from_file(filename, mime=True).decode('utf8')
    if ftype == 'text/plain':
        ftype = 'text'
    elif ftype == 'image/svg+xml':
        ftype = 'svg'
    else:
        ftype = ftype.split('/')[1]
    return ftype


def parse_configuration(config):
    '''
    Parse and fix configuration:
        - processed file should end up being same as input
        - pipelines should contain CLI commands to run
    '''
    new_config = copy.deepcopy(config)

    # Always end up with input file. If app outputs to a different one,
    # then replace old one with it
    for prog in new_config['parameters']:
        if '{output_file}' in new_config['parameters'][prog]:
            new_config['parameters'][prog] = new_config['parameters'][prog] + " && mv '{output_file}' '{file}'"

    # Build pipelines
    for label, raw_pipeline in new_config['pipelines'].items():
        commands = []
        for app in raw_pipeline:
            full_command = " ".join([new_config['commands'][app],
                                     new_config['parameters'][app]])
            commands.append(full_command)
        new_config['pipelines'][label] = " && ".join(commands)

    return new_config


def backup_file(filename, backup_ext):
    '''
    Make a file backup if:
    - backup extension is defined
    - backup file does not exist yet
    If backup file exists:
    - do nothing if it is same
    - complain loudly otherwise

    Return file name of the back up if successful. None otherwise.
    '''
    ext = backup_ext.strip(" .")
    if ext:
        backup_filename = ".".join([filename, ext])
        if not exists(backup_filename):
            shutil.copyfile(filename, backup_filename)
        else:
            if not filecmp.cmp(filename, backup_filename):
                raise DietException('Cannot make backup because a different'
                                    'file with that name already exists.')
        return backup_filename
    return None
