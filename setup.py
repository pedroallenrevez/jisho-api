from setuptools import setup, find_packages
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


# +
setup_args = dict(
    name='jisho',
    version='0.0.1',
    description='Jisho.org API helper.',
    url='https://github.com/pedroallenrevez/jisho',
    author='pedroallenrevez',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['contrib', 'docs', 'notebooks']),
    install_requires=requirements,
    entry_points = {
        'console_scripts': ['jisho=jisho.cli:make_cli']
    }
)

if __name__ == "__main__":
    setup(**setup_args)