import magic
import yaml


def read_yaml_configuration(filename):
    with open(filename, 'r') as f:
        config = yaml.load(f.read())
    return config


def determinetype(filename):
    ftype = magic.from_file(filename, mime=True).decode('utf8')
    if ftype == 'text/plain':
        ftype = 'text'
    elif ftype == 'image/svg+xml':
        ftype = 'svg'
    else:
        ftype = ftype.split('/')[1]
    return ftype
