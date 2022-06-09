# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='pyCMMT',
    version='0.1.0',
    description='Library to issue profidrive tasks for the CMMT',
    long_description=readme,
    author='Elias Rosch',
    author_email='elias.rosch@festo.com',
    url='https://gitlab.festo.company/lrsch/pycmmt',
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude="tests"),
    python_requires=">= 3.7"
)
