# -*- coding: utf-8 -*-


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
    python_requires=">= 3.7",
    install_requires=['pymodbus', 'ethernetip'],
    entry_points={
        'console_scripts': [
            'pycmmt-pnu = pycmmt_tools.pnu:main',
            'pycmmt-position = pycmmt_tools.position:main',
            'pycmmt-test-tg1 = pycmmt_tools.telegram1:main',
            'pycmmt-test-tg9 = pycmmt_tools.telegram9:main',
            'pycmmt-test-tg102 = pycmmt_tools.telegram102:main',
            'pycmmt-test-tg111 = pycmmt_tools.telegram111:main',
        ],
    },
)
