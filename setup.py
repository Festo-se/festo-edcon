# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='pyCMMT',
    description='Library to issue profidrive tasks for the CMMT',
    long_description=readme,
    author='Elias Rosch',
    author_email='elias.rosch@festo.com',
    url='https://gitlab.festo.company/lrsch/pycmmt',
    use_scm_version=True,
    python_requires=">= 3.7",
    setup_requires=["setuptools_scm"],
    install_requires=['pymodbus', 'ethernetip'],
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude="tests"),
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
