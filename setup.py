from setuptools import setup, find_packages

long_description = '''\
pyimagediet is a Python wrapper around image optimisations tools used to
reduce images size without loss of visual quality. It provides a uniform
interface to tools, easy configuration and integration.

It works on images in JPEG, GIF and PNG formats and will leave others
unchanged.'''

setup(
    author="Marko Samastur",
    author_email="markos@gaivo.net",
    name='pyimagediet',
    version='0.5',
    description='Python wrapper around image optimisations tools',
    long_description=long_description,
    url='https://github.com/samastur/pyimagediet/',
    platforms=['OS Independent'],
    license='MIT License',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    install_requires=[
        'PyYAML>=3.11',
        'python-magic>=0.4.10',
    ],
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False
)
