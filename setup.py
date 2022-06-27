import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = long_description.split("</p>")[1]
    long_description = "# OUTATIME" + long_description

setuptools.setup(
    name='outatime',
    packages=setuptools.find_packages(),
    version='3.1.0',
    description='Python framework to manage time series.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Luca Spartera',
    author_email='synstratos.dev@gmail.com',
    url='https://github.com/SynStratos/outatime',
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
