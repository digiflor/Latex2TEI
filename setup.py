#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages

setup(
    name='latex2tei',
    version="0.1.9",
    #py_modules=['latex2tei'],
    include_package_data=True,
    packages=find_packages(),
    scripts=["latex2tei.py"],
    author="Marta Materni",
    author_email="marta.materni@gmail.com",
    description="Tools per Latex  => TEI ",
    url='https://github.com/digiflor/',
    license="new BSD License",
    install_requires=[],
    classifiers=['Development Status :: 1 - Planing',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: Italiano',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python 3.7.0',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities']
)
