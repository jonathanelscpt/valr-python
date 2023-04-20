#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='valr-python',
    version='0.3.0',
    license='MIT',
    description='Python SDK for the VALR REST API',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Jonathan Els',
    author_email='jonathanelscpt@gmail.com',
    url='https://github.com/jonathanelscpt/valr-python',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    project_urls={
        'Changelog': 'https://github.com/jonathanelscpt/valr-python/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'https://github.com/jonathanelscpt/valr-python/issues',
    },
    keywords=[
        'VALR', 'REST', 'API', 'Bitcoin', 'Ethereum', 'stream', 'websocket',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests', 'websockets', 'asyncio', 'simplejson',
    ],
    tests_require=['pytest', 'pytest-cov', 'requests_mock'],
    extras_require={
    },
)
