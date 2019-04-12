# coding: utf-8
from setuptools import setup, find_packages
import os


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


__version__ = "0.1.4"

setup(
    name='slaveaccount',
    version=__version__,
    keywords='',
    description='',
    long_description=read("README.md"),

    url='https://github.com/lamter/slaveaccount',
    author='lamter',
    author_email='lamter.fu@gmail.com',

    packages=find_packages(),
    package_data={

    },
    install_requires=read("requirements.txt").splitlines(),
    classifiers=['Development Status :: 1 - Alpha',
                 'Programming Language :: Python :: 3.7',
                 'License :: OSI Approved :: MIT'],
)
