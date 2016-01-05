import os
import pyimagediet.helpers as helpers


TOOLS_DIR = os.getenv('DIET_TOOLS_DIR', '/usr/local/bin')


def test_find_tools_returns_empty_dict_if_no_tools_are_found():
    tools = ('fakeoptipng',)
    cmds = helpers.find_tools(tools)
    assert cmds == {}


def test_find_tools_finds_them():
    tools = ('optipng',)
    cmds = helpers.find_tools(tools)

    path = os.path.join(TOOLS_DIR, 'optipng')
    assert cmds['optipng'] == path


def test_cmds_to_pipelines_returns_correct_dict_when_tools_present():
    commands = {
        'optipng': 'optipng',
        'pngcrush': 'pngcrush',
        'gifsicle': 'gifsicle',
        'jpegoptim': 'jpegoptim',
    }
    expected = {
        'png': ['optipng', 'pngcrush'],
        'gif': ['gifsicle'],
        'jpeg': ['jpegoptim']
    }
    output = helpers.cmds_to_pipelines(commands)
    assert output == expected


def test_section_to_yaml_returns_empty_string_when_given_no_commands():
    output = helpers.section_to_yaml('commands', {})
    assert output == ""


def test_section_to_yaml_returns_correct_yaml_when_tools_present():
    tools = {
        'advpng': '/bin/advpng',
        'optipng': '/bin/optipng',
    }
    expected = """\
commands:
  advpng: /bin/advpng
  optipng: /bin/optipng
"""
    output = helpers.section_to_yaml('commands', tools)
    assert output == expected


def test_get_config_output(capsys):
    expected = """\
commands:
  optipng: {0}/optipng
pipelines:
  png:
  - optipng

""".format(TOOLS_DIR)

    helpers.TOOLS = ('optipng',)

    helpers.get_config()
    output, err = capsys.readouterr()
    assert output == expected
