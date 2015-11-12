import copy
from os.path import abspath, dirname, join
import pytest

import pyimagediet.diet as diet

TEST_DIR = abspath(dirname(__file__))
TEST_CONFIG = {
	'commands': {
		'advpng': '/usr/local/bin/advpng',
		'gifsicle': '/usr/local/bin/gifsicle',
		'jpegoptim': '/usr/local/bin/jpegoptim',
		'jpegtran': '/usr/local/bin/jpegtran',
		'optipng': '/usr/local/bin/optipng',
		'pngcrush': '/usr/local/bin/pngcrush'},
	'parameters': {
		'advpng': "-z4 '{file}s'",
		'gifsicle': "-O2 '{file}' > '{output_file}'",
		'jpegoptim': "-f --strip-all '{file}s'",
		'jpegtran': "-copy none -progressive -optimize -outfile '{output_file}' '{file}'",
		'optipng': "-force -o7 '{file}'",
		'pngcrush': "-rem gAMA -rem alla -rem cHRM -rem iCCP -rem sRGB -rem time '{file}' '{output_file}'"},
	'pipelines': {
		'gif': ['gifsicle'],
		'jpeg': ['jpegtran'],
		'png': ['optipng', 'advpng', 'pngcrush']}}


@pytest.fixture
def config_copy():
	return copy.deepcopy(TEST_CONFIG)


def test_read_yaml_configuration():
    f = join(TEST_DIR, 'test_files/config.yaml')
    config = diet.read_yaml_configuration(f)
    assert isinstance(config, dict)


def test_determinetype_returns_text_on_yaml():
    f = join(TEST_DIR, 'test_files/config.yaml')
    ftype = diet.determinetype(f)
    assert ftype == 'text'


def test_determinetype_returns_png_on_png_images():
    f = join(TEST_DIR, 'test_files/nature.png')
    ftype = diet.determinetype(f)
    assert ftype == 'png'


def test_determinetype_returns_gif_on_gif_images():
    f = join(TEST_DIR, 'test_files/nature.gif')
    ftype = diet.determinetype(f)
    assert ftype == 'gif'


def test_determinetype_returns_jpeg_on_jpeg_images():
    f = join(TEST_DIR, 'test_files/vienna.jpg')
    ftype = diet.determinetype(f)
    assert ftype == 'jpeg'


def test_determinetype_returns_svg_on_svg_images():
    f = join(TEST_DIR, 'test_files/nature.svg')
    ftype = diet.determinetype(f)
    assert ftype == 'svg'


def test_parse_configuration_correctly_handles_output_file(config_copy):
	corrected = {
		'gifsicle': "-O2 '{file}' > '{output_file}' && mv '{output_file}' '{file}'",
		'jpegtran': "-copy none -progressive -optimize -outfile '{output_file}' '{file}' && mv '{output_file}' '{file}'",
		'pngcrush': "-rem gAMA -rem alla -rem cHRM -rem iCCP -rem sRGB -rem time '{file}' '{output_file}' && mv '{output_file}' '{file}'"
	}
	config = diet.parse_configuration(config_copy)
	for prog, params in config['parameters'].items():
		if '{output_file}' in params:
			assert params == corrected[prog]


def test_parse_configuration_correctly_builds_pipelines(config_copy):
	config = diet.parse_configuration(config_copy)
	pipelines = {
		'gif': (
			"/usr/local/bin/gifsicle -O2 '{file}' > '{output_file}' "
			"&& mv '{output_file}' '{file}'"),
		'jpeg': (
			"/usr/local/bin/jpegtran -copy none -progressive -optimize -outfile "
			"'{output_file}' '{file}' && mv '{output_file}' '{file}'"),
		'png': (
			"/usr/local/bin/optipng -force -o7 '{file}' "
			"&& /usr/local/bin/advpng -z4 '{file}s' "
			"&& /usr/local/bin/pngcrush -rem gAMA -rem alla -rem cHRM -rem iCCP "
			"-rem sRGB -rem time '{file}' '{output_file}' && mv '{output_file}' "
			"'{file}'")
	}
	for img_type, pipeline in config['pipelines'].items():
		assert pipeline == pipelines[img_type]

