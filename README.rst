.. _start-intro:

#######################################################################
outatime: a python framework to manage time series.
#######################################################################
|pypi_ver| |test_status| |cover_status| |dependencies|
|github_issues| |python_ver| |proj_license| |pypi_downloads|

:release:       3.1.0
:date:          2022-05-10 10:30:00
:repository:    https://github.com/synstratos/outatime
:pypi-repo:     https://pypi.org/project/outatime/
:docs:          https://outatime.readthedocs.io/
:keywords:      time, time-series, time series, time series data
:developers:    .. include:: AUTHORS.rst

.. _end-intro:

.. _start-about:
.. _start-0-pypi:
About outatime
==============
The main goal of this framework is to simplify the collection of temporal data
and related operations.
It is based on the concepts of **TimeSeries**, as a collection of records
associated with a given day, and **Granularity**, to indicate a given time
interval (e.g. daily, weekly, monthly, etc.).

The object related to a single day (**TimeSeriesData**) contains two attributes:

* **day** - the reference date for that record
* **data** - an object that collects any information for that day

Why outatime?
-------------
Outatime allows to carry out numerous operations of different types on time series,
as for example:

* add or remove records
* search records by date
* exclude records outside a determined range
* resampling of data
* querying data
* union and intersection
* batch splitting and data aggregation
* other

.. _end-0-pypi:
.. _end-about:

.. _start-install:
Installation
============
To install it use:

.. code-block:: console

    $ pip install outatime

or download the last git version and use:

.. code-block:: console

    $ python setup.py install

.. _end-install:

.. _start-structure:
Framework Structure
========
.. code-block:: console

    outatime
    ├── dataclass
    │   └── time_series_data.py --> Class used to manage daily data.
    │
    ├── granularity
    │   ├── granularity.py --> Set of classes used for managing time intervals of different length.
    │   ├── granularity_factory.py --> Factory class for creating granularity objects.
    │   └── utils.py --> Utils related to granularity.
    │
    ├── timeseries
    │   ├── batches.py --> Set of methods to operate on time series dividing them into batches.
    │   ├── expr.py --> Set of operations between time series.
    │   ├── filter_parser.py --> Class that allows to parse query strings into filters.
    │   ├── inference.py --> Method to infer granularity of a time series.
    │   └── time_series.py --> Core class that represents a series of daily records.
    │
    └── util
        ├── agenda.py --> Utils related to calendar info and evaluations.
        ├── bisect.py --> Utils related to binary search.
        ├── decorators.py --> Useful decorators.
        └── relativedelta.py --> Class that extends relativedelta with useful properties.

.. _end-structure:

.. _start-tutorial:

Tutorial
========

Create a time series
-------
To create your first time series, you need to collect data in individual objects of type TimeSeriesData.
A list of these objects can be fed to our TimeSeries class.

.. code-block:: console

    ts_data = [
        TimeSeriesData(
            day = datetime.date(2022, 6, 24),
            data = {
                "AAPL": 135.73,
                "MSFT": 251.81,
                "GOOGL": 2275.34
            }
        ),
        TimeSeriesData(
            day = datetime.date(2022, 6, 27),
            data = {
                "AAPL": 142.16,
                "MSFT": 265.66,
                "GOOGL": 2337.92
            }
        )
    ]

    ts = TimeSeries(ts_data)

You can add new data to your time series, that will keep the information in chronological order.

.. code-block:: console

    new_data = TimeSeriesData(
            day = datetime.date(2022, 6, 23),
            data = {
                "AAPL": 140.04,
                "MSFT": 249.65,
                "GOOGL": 2229.44
            }
        )

    ts.append(new_data)

You can also update the time series with multiple new inputs.

.. code-block:: console

    new_data_list = [
        TimeSeriesData(
            day = datetime.date(2022, 6, 22),
            data = {
                "AAPL": 136.55,
                "MSFT": 246.07,
                "GOOGL": 2205.50
            }
        ),
        TimeSeriesData(
            day = datetime.date(2022, 6, 23),
            data = {
                "AAPL": 140.04,
                "MSFT": 249.65,
                "GOOGL": 2229.44
            }
        )
    ]

    ts.update(new_data_list)

Retrieve data
-------
There are different ways to retrieve data from your time series.

1. You can get a TimeSeriesData by its index in the TimeSeries object.

.. code-block:: console

    ts_data = ts[0]  # gets the first element in the time series

2. Alternatively you can search for an item by its date.

.. code-block:: console

    date_to_find = datetime.date(2022, 6, 23)
    ts_data = ts.get(date_to_find)  # gets the element with the given date

3. In addition, a subset of the time series can be extracted using the query function. The user can specify filters in string format to be applied on the values of "day," "month," and "year."

.. code-block:: console

    query = "month == 6 and day == 2022)
    ts_subset = ts.query(date_to_find)  # extracts all data for the month of June for the year 2022


Manage the time series
-------

Transform the time series
-------

.. _end-tutorial:

.. _start-badges:
.. |test_status| image:: https://github.com/synstratos/outatime/actions/workflows/python-package.yml/badge.svg?branch=stable
    :alt: Build status
    :target: https://github.com/synstratos/outatime/actions/workflows/python-package.yml/badge.svg?branch=stable

.. |cover_status| image:: https://coveralls.io/repos/github/synstratos/outatime/badge.svg
    :target: https://coveralls.io/github/synstratos/outatime
    :alt: Code coverage

.. |pypi_ver| image::  https://img.shields.io/pypi/v/outatime.svg?
    :target: https://pypi.python.org/pypi/outatime/
    :alt: Latest Version in PyPI

.. |python_ver| image:: https://img.shields.io/pypi/pyversions/outatime
    :target: https://pypi.python.org/pypi/outatime/
    :alt: Supported Python versions

.. |github_issues| image:: https://img.shields.io/github/issues/synstratos/outatime.svg?
    :target: https://github.com/synstratos/outatime/issues
    :alt: Issues count

.. |proj_license| image:: https://img.shields.io/github/license/synstratos/outatime
    :target: https://raw.githubusercontent.com/synstratos/outatime/stable/LICENSE
    :alt: Project License

.. |dependencies| image:: https://requires.io/github/SynStratos/outatime/requirements.svg?branch=stable
     :target: https://requires.io/github/SynStratos/outatime/requirements/?branch=stable
     :alt: Requirements Status

.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/outatime.svg?style=flat-square&label=PyPI%20Downloads
    :target: https://pypi.org/project/outatime
    :alt: Pypi Downloads

.. |conda_downloads| image:: https://img.shields.io/conda/dn/conda-forge/outatime?label=Conda%20Downloads&style=flat-square
    :target: https://anaconda.org/conda-forge/outatime
    :alt: Conda Downloads
.. _end-badges: