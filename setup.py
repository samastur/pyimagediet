import codecs
import os
import re
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

HERE = os.path.abspath(os.path.dirname(__file__))


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)


def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(HERE, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read_long_description():
    long_description = ""
    with open('README.rst', 'r') as f:
        long_description = f.read()
    return long_description


setup(
    author="Marko Samastur",
    author_email="markos@gaivo.net",
    name='pyimagediet',
    version=find_version('pyimagediet', '__init__.py'),
    description='Python wrapper around image optimisations tools',
    long_description=read_long_description(),
    url='https://github.com/samastur/pyimagediet/',
    platforms=['OS Independent'],
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=[
        'PyYAML>=3.11',
        'python-magic>=0.4.10',
        'Click>=6.2',
    ],
    include_package_data=True,
    packages=['pyimagediet'],
    entry_points={
        'console_scripts': ['diet=pyimagediet.cli:diet']
    },
    tests_require=['tox'],
    cmdclass={'test': Tox},
    zip_safe=False
)
