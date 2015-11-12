import copy
import magic
import yaml


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
