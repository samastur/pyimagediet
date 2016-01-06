from click.testing import CliRunner
import os
import pyimagediet.scripts.diet as diet
import pyimagediet.helpers as helpers

TOOLS_DIR = os.getenv('DIET_TOOLS_DIR', '/usr/local/bin')


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
