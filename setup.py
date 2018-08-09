#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='docker-compose-extension',
    version='0.0.1',
    description='Extending docker-compose with tools for networking and nginx proxy config.',
    author='Claudio Walser',
    author_email='claudio.walser@srf.ch',
    url='https://github.com/claudio-walser/python-docker-compose',
    packages=find_packages(),
    install_requires=['simpcli', 'pyyaml', 'argparse', 'argcomplete', 'shutilwhich', 'inquirer'],
    entry_points={
        'console_scripts': [
            'docker-manager = docker_manager.bin.console:main'
        ]
    }
)
