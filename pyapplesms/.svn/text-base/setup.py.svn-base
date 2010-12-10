#!/usr/bin/env python

from distutils.core import setup, Extension
import os

os.environ["CFLAGS"] = " -Wall -g -framework IOKit"

setup(
	name = 'PyAppleSMS',
	version = '1.0',
	description = 'Python module for Apple SMS (Sudden Motion Sensor)',
	long_description='''This module allows you to access in Apple SMS (Sudden Motion Sensor). SMS sensor are installed by default in all new Apple laptops and it returns x, y, z coordinates about laptop movements.
	For more informations read this page of Wikipedia: http://en.wikipedia.org/wiki/Sudden_Motion_Sensor''',
	author='Michele Ferretti',
	author_email='michele.ferretti@gmail.com',
	url='http://www.blackbirdblog.it/progetti/pyapplesms',
	download_url='http://www.blackbirdblog.it/download/software/PyAppleSMS-1.0.tar.gz',
	classifiers=[
		'Classifier: Environment :: MacOS X',
		'Classifier: Operating System :: MacOS :: MacOS X',
		'Classifier: Topic :: Scientific/Engineering :: Human Machine Interfaces',
		'Classifier: Topic :: Software Development :: Libraries',
		'Classifier: Topic :: Software Development :: Libraries :: Python Modules',
		'Classifier: Topic :: System :: Hardware'
	],
	ext_modules = [Extension('applesms', sources = ['applesms.c'])]
)

