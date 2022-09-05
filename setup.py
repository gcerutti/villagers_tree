#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

short_descr = "A python package to generate a tree visualization of Villagers cards."
readme = open('README.md').read()

# find packages
pkgs = find_packages('src')

setup_kwds = dict(
    name='villagers_tree',
    version="0.1.0",
    description=short_descr,
    long_description=readme,
    author="Guillaume Cerutti",
    author_email="guillaume.cerutti@gmail.com",
    url='',
    license='LGPL-3.0',
    zip_safe=False,

    packages=pkgs,

    package_dir={'': 'src'},
    entry_points={
        'console_scripts':[
            "generate_villager_cards = villagers_tree.scripts.generate_villager_cards:main"
        ]
    },
    keywords='',
)

setup(**setup_kwds)
