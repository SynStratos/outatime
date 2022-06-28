import io
import os
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


setuptools.setup(
    packages=setuptools.find_packages(),
    version="3.2.0", #read_project_version(),
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
