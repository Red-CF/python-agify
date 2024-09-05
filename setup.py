from setuptools import setup, find_packages
import re
import io
import os

here = os.path.abspath(os.path.dirname(__file__))

# get version from module source
version = None
version_re = re.compile(r"^__version__ = '(.*?)'$")
with open(os.path.join(here, 'agify/__init__.py')) as f:
    for line in f:
        match = version_re.match(line)
        if match:
            version = match.group(1)
            break

# get long desc from README.rst
with io.open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='Python-Agify',
    version=version,
    description='Python client for Agify.io web service.',
    long_description=long_description,
    author='Carlos Rojas or RED',
    license='MIT',
    url='',
    packages=find_packages(),
    install_requires=[
        'requests >= 1.0.0',
    ],
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)