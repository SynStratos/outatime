.. _start-intro:

#######################################################################
outatime: Python Framework to Manage Time Series.
#######################################################################
|pypi_ver| |test_status| |cover_status| |docs_status| |dependencies|
|github_issues| |python_ver| |proj_license| |binder|

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
* day - the reference date for that record
* data - an object that collects any information for that day

Why outatime?
-------------
Outatime allows to carry out numerous operations of different types on time series,
as for example:
* add or remove records
* search records by date
* exclude records outside a determined range
* resampling of data
* union and intersection
* batch splitting and data aggregation
* other

.. _end-0-pypi:
.. _end-about:

.. _start-install:
Installation
============
To install it use (with root privileges):

.. code-block:: console

    $ pip install outatime

or download the last git version and use (with root privileges):

.. code-block:: console

    $ python setup.py install

.. _end-install:

.. _start-structure:
Framework Structure
========
.. code-block::
    outatime
    ├── dataclass
    │   └── time_series_data.py --> Class used to manage daily data.
    │
    ├── granularity
    │   ├── granularity.py --> Set of classes used for managing time intervals of different length.
    │   ├── granularity_factory.py --> Factory class for creating granularity objects.
    │   └── utils.py --> Utils related to granularities.
    │
    ├── timeseries
    │   ├── batches.py --> Set of methods to operate on time series dividing them into batches.
    │   ├── expr.py --> Set of operations between time series.
    │   ├── filter_parser.py --> Class that allows to parse query strings into filters.
    │   ├── inference.py --> Method to infer granularity of a time series.
    │   └── time_series.py --> Core class that represents a series of daily records.
    │
    └── util
        ├── agenda.py --> Utils related to calendar info and evalutations.
        ├── bisect.py --> Utils related to binary search.
        ├── decorators.py --> Useful decorators.
        └── relativedelta.py --> Class that extends relativedelta with useful properties.

.. _end-structure:

.. _start-tutorial:

Tutorial
========

.. _end-tutorial: