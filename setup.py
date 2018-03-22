import os
import sys
from setuptools import find_packages, setup

def get_requirements():
    with open('requirements.txt') as fp:
        return [x.strip() for x in fp.read().split('\n') if not x.startswith('#')]

setup(
    name="Twitter Sentiment Analysis",
    version="0.0.1",
    description='Sentiment analysis on California wildfire tweets',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=get_requirements(),
    license="Apache License 2.0",
)
