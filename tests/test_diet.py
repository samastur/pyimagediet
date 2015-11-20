import copy
import filecmp
import os
from os.path import abspath, dirname, join, exists
import pytest
import shutil

import pyimagediet.diet as diet

TEST_DIR = abspath(dirname(__file__))
TEST_FILES_DIR = join(TEST_DIR, 'test_files')
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
BALLOON_CMD = join(TEST_DIR, 'balloon.py')


@pytest.fixture
def config_copy():
	return copy.deepcopy(TEST_CONFIG)


def test_read_yaml_configuration():
    f = join(TEST_FILES_DIR, 'config.yaml')
    config = diet.read_yaml_configuration(f)
    assert isinstance(config, dict)


#
# determine_type
#
def test_determine_type_returns_text_on_yaml():
    f = join(TEST_FILES_DIR, 'config.yaml')
    ftype = diet.determine_type(f)
    assert ftype == 'text'


def test_determine_type_returns_png_on_png_images():
    f = join(TEST_FILES_DIR, 'nature.png')
    ftype = diet.determine_type(f)
    assert ftype == 'png'


def test_determine_type_returns_gif_on_gif_images():
    f = join(TEST_FILES_DIR, 'nature.gif')
    ftype = diet.determine_type(f)
    assert ftype == 'gif'


def test_determine_type_returns_jpeg_on_jpeg_images():
    f = join(TEST_FILES_DIR, 'vienna.jpg')
    ftype = diet.determine_type(f)
    assert ftype == 'jpeg'


def test_determine_type_returns_svg_on_svg_images():
    f = join(TEST_FILES_DIR, 'nature.svg')
    ftype = diet.determine_type(f)
    assert ftype == 'svg'


#
# parse_configuration
#
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


#
# Check configuration
#
def test_check_configuration_passes_on_test_config(config_copy):
    diet.check_configuration(config_copy)


def test_check_configuration_fails_if_section_is_missing():
    sections = ('commands', 'parameters', 'pipelines')
    for section in sections:
        config = config_copy()
        del config[section]
        try:
            diet.check_configuration(config)
        except (diet.ConfigurationErrorDietException,) as e:
            error_msg = 'Error: Section {} is missing.'.format(section)
            assert e.msg == error_msg


def test_check_configuration_fails_if_sections_are_malformed():
    sections = ('commands', 'parameters', 'pipelines')
    for section in sections:
        config = config_copy()
        config[section] = 'not a dict'
        try:
            diet.check_configuration(config)
        except (diet.ConfigurationErrorDietException,) as e:
            error_msg = 'Error: Section {} is malformed.'.format(section)
            assert e.msg == error_msg

def test_check_configuration_fails_if_tools_in_commands_and_parameters_differ():
    sections = ('commands', 'parameters')
    for section in sections:
        config = config_copy()
        del config[section]['advpng']
        try:
            diet.check_configuration(config)
        except (diet.ConfigurationErrorDietException,) as e:
            error_msg = ('Every command in commands and parameters section has'
                         ' to have a corresponding entry in the other section.')
            assert e.msg == error_msg


def test_check_configuration_fails_if_pipelines_are_malformed(config_copy):
    pipelines = config_copy['pipelines']

    pipelines['gifsicle'] = 'gifsicle'
    try:
        diet.check_configuration(config_copy)
    except (diet.ConfigurationErrorDietException,) as e:
        error_msg = ('Error: Pipeline gifsicle is malformed. Values have to '
                     'be a list of command names.')
        assert e.msg == error_msg

    pipelines['gifsicle'] = ['gifsicled']
    try:
        diet.check_configuration(config_copy)
    except (diet.ConfigurationErrorDietException,) as e:
        error_msg = ('Error in pipeline gifsicle. "gifsicled" cannot be found '
                     'among commands listed in commands section')
        assert e.msg == error_msg


#
# backup_file
#
def test_backup_file_does_nothing_without_extension():
	backup = diet.backup_file('madeup_file.txt', '')
	assert backup is None


def test_backup_file_creates_backup_with_extension_if_it_does_not_exist_yet():
	filename = join(TEST_FILES_DIR, 'config.yaml')
	backup_filename = ".".join([filename, 'back'])

	assert not exists(backup_filename)

	result = diet.backup_file(filename, 'back')

	assert result == backup_filename
	assert exists(backup_filename)

	os.remove(backup_filename)


def test_backup_file_does_not_complain_if_backup_already_exists():
	filename = join(TEST_FILES_DIR, 'config.yaml')
	backup_filename = ".".join([filename, 'back'])

	result = diet.backup_file(filename, 'back')
	assert result == backup_filename

	result2 = diet.backup_file(filename, 'back')
	assert result2 == backup_filename
	assert exists(backup_filename)

	os.remove(backup_filename)


def test_backup_file_raises_exception_if_different_backup_exists():
	filename = join(TEST_FILES_DIR, 'config.yaml')
	backup_filename = ".".join([filename, 'back'])
	shutil.copy(join(TEST_FILES_DIR,  'nature.gif'), backup_filename)

	try:
		result = diet.backup_file(filename, 'back')
	except (diet.DietException,) as e:
		pass

	os.remove(backup_filename)


#
# copy_if_different
#
def test_copy_if_different_does_nothing_if_files_are_same():
    filename = join(TEST_FILES_DIR, 'config.yaml')
    copy_filename = ".".join([filename, 'back'])
    shutil.copyfile(filename, copy_filename)

    statinfo = os.stat(copy_filename)
    diet.copy_if_different(filename, copy_filename)
    assert os.stat(copy_filename) == statinfo

    os.remove(copy_filename)


def test_copy_if_different_copies_file_if_destination_is_different():
    filename = join(TEST_FILES_DIR, 'config.yaml')
    copy_filename = ".".join([filename, 'back'])
    with open(copy_filename, 'w') as f:
        f.write('almost empty')

    statinfo = os.stat(copy_filename)
    diet.copy_if_different(filename, copy_filename)
    assert os.stat(copy_filename) != statinfo

    os.remove(copy_filename)


#
# squeeze
#
def test_squeeze_restores_file_if_it_fails():
    orig_filename = join(TEST_FILES_DIR, 'nature.gif')
    backup = diet.backup_file(orig_filename, 'test')
    filename = ".".join([orig_filename, "test"])
    backup = diet.backup_file(filename, 'back')
    stat = os.stat(filename)

    # Screw up file
    with open(filename, 'w') as f:
        f.write(" ")

    assert not filecmp.cmp(filename, backup)

    # This will fail because of missing command AND broken image
    size = diet.squeeze('no_command', filename, backup)

    assert size == stat.st_size
    assert filecmp.cmp(filename, backup)

    os.remove(backup)
    os.remove(filename)


def test_squeeze_shrinks_an_image():
    filename = join(TEST_FILES_DIR, 'nature.png')
    backup = diet.backup_file(filename, 'back')
    stat = os.stat(filename)
    cmd = "optipng -force -o7 '{file}' "

    assert filecmp.cmp(filename, backup)

    size = diet.squeeze(cmd, filename, "")
    assert not filecmp.cmp(filename, backup)

    shutil.copyfile(backup, filename)
    os.remove(backup)


#
# diet
#
def add_fake_pipeline_to_config(cmd, conf):
    conf['commands']['balloon'] = cmd
    conf['parameters']['balloon'] = '{file} "more bytes"'
    conf['pipelines']['text'] = ['balloon']


def test_diet_complains_if_passed_filename_is_not_file():
    filename = TEST_FILES_DIR

    try:
        diet.diet(filename, {})
    except (diet.NotFileDietException,) as e:
        pass


def test_diet_creates_a_backup_file_if_backup_is_enabled(config_copy):
    filename = join(TEST_FILES_DIR, 'nature.png')
    backup_filename = ".".join([filename, 'back'])
    config_copy['backup'] = 'back'

    diet.diet(filename, config_copy)

    assert exists(backup_filename)
    os.remove(backup_filename)


def test_diet_removes_all_backup_files_if_backup_is_disabled(config_copy):
    filename = join(TEST_FILES_DIR, 'nature.png')
    backup_filename = ".".join([filename, 'back'])
    internal_filename = ".".join([filename, 'diet_internal'])

    diet.diet(filename, config_copy)

    assert not exists(backup_filename)
    assert not exists(internal_filename)


def test_diet_deletes_internal_backup_when_backup_is_disabled(config_copy):
    filename = join(TEST_FILES_DIR, 'config.yaml')
    backup_filename = ".".join([filename, 'diet_internal'])

    diet.diet(filename, config_copy)
    assert not exists(backup_filename)


def test_diet_doesnt_change_files_without_pipeline(config_copy):
    filename = join(TEST_FILES_DIR, 'config.yaml')

    statinfo = os.stat(filename)

    diet.diet(filename, config_copy)
    assert os.stat(filename) == statinfo


def test_diet_keeps_smaller_file_by_default(config_copy):
    add_fake_pipeline_to_config(BALLOON_CMD, config_copy)
    orig_filename = join(TEST_FILES_DIR, 'config.yaml')
    diet.backup_file(orig_filename, 'test')
    filename = ".".join([orig_filename, "test"])

    old_size = os.stat(filename).st_size

    diet.diet(filename, config_copy)
    assert os.stat(filename).st_size == old_size

    os.remove(filename)


def test_diet_keeps_processed_file_if_keep_processed_is_enabled(config_copy):
    add_fake_pipeline_to_config(BALLOON_CMD, config_copy)
    config_copy['keep_processed'] = True
    orig_filename = join(TEST_FILES_DIR, 'config.yaml')
    diet.backup_file(orig_filename, 'test')
    filename = ".".join([orig_filename, "test"])

    old_size = os.stat(filename).st_size

    diet.diet(filename, config_copy)
    assert os.stat(filename).st_size > old_size

    os.remove(filename)
