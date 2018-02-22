"""A setuptools based setup module.
See:
   https://github.com/pypa/sampleproject/blob/master/setup.py
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='flask_blog',
    version='0.1.dev1',
    description='A blog application using Flask',
    long_description=long_description,
    url='https://github.com/npmarrin/flask-blog',
    author='Nathaniel P. Marrin',
    packages=['flask_blog'],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a string of words separated by whitespace, not a list.
    keywords='flask sqlalchemy',
)
