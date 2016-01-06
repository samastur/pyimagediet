from click.testing import CliRunner
import filecmp
import os
from os.path import abspath, dirname, join
import shutil

import pyimagediet.scripts.diet as diet
import pyimagediet.process as process
import pyimagediet.helpers as helpers

TOOLS_DIR = os.getenv('DIET_TOOLS_DIR', '/usr/local/bin')
TEST_DIR = abspath(dirname(__file__))
TEST_FILES_DIR = join(TEST_DIR, 'test_files')
TEST_FILE = join(TEST_FILES_DIR, 'nature.png')
TEST_CONFIG = join(TEST_FILES_DIR, 'config2.yaml')


def test_diet_check_option_prints_configuration():
    expected = """\
commands:
  optipng: {0}/optipng
pipelines:
  png:
  - optipng

""".format(TOOLS_DIR)

    helpers.TOOLS = ('optipng',)

    runner = CliRunner()
    result = runner.invoke(diet.diet, ['--check'])
    assert result.output == expected
    assert result.exit_code == 0


def test_diet_complains_if_no_configuration_provided():
    err = 'Usage: diet [OPTIONS] FILE\n\nError: Missing option "--config".\n'
    runner = CliRunner()
    result = runner.invoke(diet.diet, [TEST_FILE])
    assert result.output == err
    assert result.exit_code == 2


def test_diet_complains_if_no_file_is_provided():
    err = 'Usage: diet [OPTIONS] FILE\n\nError: Missing argument "file".\n'

    runner = CliRunner()
    result = runner.invoke(diet.diet, ['--config', TEST_CONFIG])
    assert result.output == err
    assert result.exit_code == 2


def test_diet_squeezes_file():
    backup = process.backup_file(TEST_FILE, 'back')

    assert filecmp.cmp(TEST_FILE, backup)

    try:
        runner = CliRunner()
        result = runner.invoke(diet.diet, ['--config', TEST_CONFIG, backup])
        assert not filecmp.cmp(TEST_FILE, backup)
        assert result.exit_code == 0
    finally:
        os.remove(backup)
