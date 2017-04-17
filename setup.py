VERSION = '0.0.1'

import sys

from setuptools import setup

extra_args = {}
if (sys.version_info[0] >= 3):
    extra_args['use_2to3'] = True

setup(name='iq2mongo',
      version=VERSION,
      description='iq2mongo',
      author='Alex Orion',
      url='https://github.com/quantmatic/iq2mongo/',
      packages=['iq2mongo'],
      install_requires=['pymongo',
                        'pandas>=0.19'],
      **extra_args)
