from distutils.spawn import find_executable
import yaml


# List of popular external tools to search for
TOOLS = (
    'jpegoptim',
    'jpegtran',
    'gifsicle',
    'optipng',
    'advpng',
    'pngcrush',
)

# Preferred pipelines. Feels like they (as tools) should be saved in
# external file, but can't think of a benefit of doing so.
PIPELINES = {
    'png': ['optipng', 'advpng', 'pngcrush'],
    'gif': ['gifsicle'],
    'jpeg': ['jpegtran', 'jpegoptim']
}


def find_tools(tools):
    commands = {}
    for tool in tools:
        path = find_executable(tool)  # Empty string if not found
        if path:
            commands[tool] = path
    return commands


def cmds_to_pipelines(commands):
    found = set([x for x in commands])
    pipelines = {}
    for name in PIPELINES:
        pipelines[name] = [x for x in PIPELINES[name] if x in found]
        if not len(pipelines[name]):
            del pipelines[name]
    return pipelines


def section_to_yaml(section, commands):
    output = ""
    if commands:
        section = {section: commands}
        output = yaml.dump(section, default_flow_style=False)
    return output


def get_config():
    commands = find_tools(TOOLS)
    pipelines = cmds_to_pipelines(commands)
    output = section_to_yaml('commands', commands)
    output += section_to_yaml('pipelines', pipelines)
    return output
