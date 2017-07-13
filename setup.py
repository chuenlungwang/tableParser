# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='parser',
    version='0.1.0',
    description='Table parser of Excel to several language',
    long_description=readme,
    author='Zoro Wang',
    author_email='chuenlungwang@qq.com',
    url='https://github.com/chuenlungwang/tableParser',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)