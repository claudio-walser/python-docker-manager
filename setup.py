#!/usr/bin/env python3

from setuptools import setup, find_packages

def read(fpath):
    with open(fpath, 'r') as f:
        return f.read()

def version(fpath):
    return read(fpath).strip()

setup(
    name='docker-manager',
    version=version(),
    description='Extending docker-compose with tools for networking and nginx proxy config.',
    long_description=read('README.rst'),
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
