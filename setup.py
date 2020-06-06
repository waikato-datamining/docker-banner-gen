# setup.py
# Copyright (C) 2020 University of Waikato, Hamilton, NZ

from setuptools import setup


def _read(f):
    """
    Reads in the content of the file.
    :param f: the file to read
    :type f: str
    :return: the content
    :rtype: str
    """
    return open(f, 'rb').read()


setup(
    name="docker-banner-gen",
    description="Command-line tool for generating bash.bashrc templates for docker with a custom banner.",
    long_description=(
        _read('DESCRIPTION.rst') + b'\n' +
        _read('CHANGES.rst')).decode('utf-8'),
    url="https://github.com/waikato-datamining/docker-banner-gen",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Shells',
        'Programming Language :: Python :: 3',
    ],
    license='Apache 2.0',
    package_dir={
        '': 'src'
    },
    packages=[
        "dbg",
    ],
    version="0.0.2",
    author='Peter Reutemann',
    author_email='fracpete@waikato.ac.nz',
    install_requires=[
        "pyfiglet",
    ],
    entry_points={
        "console_scripts": [
            "docker-banner-gen=dbg.generate:sys_main",
        ]
    }
)
