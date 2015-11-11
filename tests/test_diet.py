from os.path import abspath, dirname, join
import pyimagediet.diet as diet

TEST_DIR = abspath(dirname(__file__))


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
