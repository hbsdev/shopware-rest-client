#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

with open('README.rst') as readme_file:
  readme = readme_file.read()

with open('HISTORY.rst') as history_file:
  history = history_file.read().replace('.. :changelog:', '')

requirements = [
  # TODO: put package requirements here
]

test_requirements = [
  # TODO: put package test requirements here
]


# (pytest A) from https://pytest.org/latest/goodpractises.html#integrating-with-distutils-python-setup-py-test
from distutils.core import setup, Command
# you can also import from setuptools

class PyTest(Command):
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    import subprocess
    import sys
    errno = subprocess.call([sys.executable, 'runtests.py'])
    raise SystemExit(errno)


setup(
  name = 'shopware_rest_client',
  version = '0.2.0',
  description = "Python 3 client library for Shopware 4 REST API",
  long_description = readme + '\n\n' + history,
  author = "Kurt Miebach",
  author_email = 'kwmiebach@gmail.com',
  url = 'https://github.com/miebach/shopware_rest_client',
  packages = [
    'shopware_rest_client',
  ],
  package_dir = {'shopware_rest_client':
    'swapi'},
  include_package_data = True,
  install_requires = requirements,
  license = "Apache 2.0",
  zip_safe = False,
  keywords = 'shopware api rest client swapi',
  classifiers = [  # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: Apache 2.0  License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Operating System :: Unix',
    'Operating System :: MacOS X',  # Classifier not official
    'Operating System :: POSIX',
    'Operating System :: POSIX :: BSD',
    'Operating System :: POSIX :: Linux',
    'Operating System :: POSIX :: Other',
    'Operating System :: POSIX :: SunOS/Solaris',
  ],

  # (pytest B) from https://pytest.org/latest/goodpractises.html#integrating-with-distutils-python-setup-py-test
  cmdclass = {'test': PyTest},

  test_suite = 'tests',
  tests_require = test_requirements
)



