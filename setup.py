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
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
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
