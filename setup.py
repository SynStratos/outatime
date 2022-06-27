import io
import os
import collections
import setuptools

name = 'outatime'
mydir = os.path.dirname(__file__)
description = 'Python framework to manage time series.'

# Version-trick to have version-info in a single place,
# taken from: http://stackoverflow.com/questions/2058802/how-can-i-get-the-
# version-defined-in-setup-py-setuptools-in-my-package

def read_project_version():
    fglobals = {}
    with io.open(os.path.join(mydir, name, '_version.py'), encoding='UTF-8') as fd:
        exec(fd.read(), fglobals)  # To read __version__
    return fglobals['__version__']


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = long_description.split("</p>")[1]
    long_description = "# OUTATIME" + long_description

setuptools.setup(
    name=name,
    packages=setuptools.find_packages(),
    version=read_project_version(),
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Luca Spartera',
    author_email='synstratos.dev@gmail.com',
    url=f'https://github.com/SynStratos/{name}',
    python_requires='>=3.8, <3.11',
    include_package_data=True,
    classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Natural Language :: English",
    ],
    keywords=['time series', 'ts', 'timeseries', 'temporal data'],
    install_requires=[
        'python-dateutil',
        'statsmodels',
        'numpy',
        'scipy',
        'lark'
    ]
)
