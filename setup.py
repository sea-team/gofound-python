# -*- coding: utf-8 -*-
import sys

from setuptools import setup
import gofound

if sys.version_info < (3, 0):

    long_description = "\n".join([
        open('README.rst', 'r').read(),
    ])
else:
    long_description = "\n".join([
        open('README.rst', 'r', encoding='utf-8').read(),
    ])

setup(
    name='gofound',
    version=gofound.get_version(),
    packages=['gofound'],
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/newpanjing/gofound-python',
    license='Apache License 2.0',
    author='panjing',
    long_description=long_description,
    author_email='newpanjing@icloud.com',
    description='gofound全文检索python客户端',
    install_requires=['requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
