# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='festo-edcon',
    description='Library to issue profidrive tasks for Festo specific electrical drives',
    long_description=readme,
    author='Elias Rosch',
    author_email='elias.rosch@festo.com',
    url='https://gitlab.com/festo-research/electric-automation/festo-edcon',
    license='MIT',
    use_scm_version=True,
    python_requires=">= 3.7",
    setup_requires=["setuptools_scm"],
    install_requires=['pymodbus<3.0.0', 'ethernetip', 'rich'],
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude="tests"),
    entry_points={
        'console_scripts': [
            'festo-edcon-position = edcon_tools.position:main',
            'festo-edcon-pnu = edcon_tools.pnu:main',
            'festo-edcon-test-tg1 = edcon_tools.test_tg1:main',
            'festo-edcon-test-tg9 = edcon_tools.test_tg9:main',
            'festo-edcon-test-tg102 = edcon_tools.test_tg102:main',
            'festo-edcon-test-tg111 = edcon_tools.test_tg111:main',
        ],
    },
)
