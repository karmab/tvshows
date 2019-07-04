# coding=utf-8
from setuptools import setup, find_packages

import os
description = 'Tvshows dummy app'
long_description = description
if os.path.exists('README.rst'):
    long_description = open('README.rst').read()

setup(
    name='tvshows',
    version='0.2',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    description=description,
    long_description=long_description,
    url='http://github.com/karmab/tvshows',
    author='Karim Boumedhel',
    author_email='karimboumedhel@gmail.com',
    license='ASL',
    install_requires=['flask', 'kubernetes', 'tvdbsimple'],
    entry_points='''
        [console_scripts]
        tvshows=tvshows.web:run
    ''',
)
