import os
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.0.1'

setup(
    name='seqtolang',
    version=VERSION,
    description="Multi Langauge Documents Langauge identification",
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hiredscorelabs/seqtolang",
    keywords='',
    license='Apache',
    packages=find_packages(exclude=['test*']),
    install_requires=[
        'torch==1.1.0',
    ],
)
