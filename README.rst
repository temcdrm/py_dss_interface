========
Overview
========

The py-dss-interface is a Python package that provides a Python interface to the OFFICIAL version of OpenDSS (Open-source Distribution System Simulator) software. OpenDSS is a free, open-source software for simulating and analyzing power distribution systems.

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |appveyor|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions|
.. |docs| image:: https://readthedocs.org/projects/py_dss_interface/badge/?style=flat
    :target: https://readthedocs.org/projects/py_dss_interface
    :alt: Documentation Status

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/PauloRadatz/py_dss_interface?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/PauloRadatz/py_dss_interface

.. |codecov| image:: https://codecov.io/gh/PauloRadatz/py_dss_interface/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/PauloRadatz/py_dss_interface

.. |version| image:: https://img.shields.io/pypi/v/py-dss-interface.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/py-dss-interface

.. |wheel| image:: https://img.shields.io/pypi/wheel/py-dss-interface.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/py-dss-interface

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/py-dss-interface.svg
    :alt: Supported versions
    :target: https://pypi.org/project/py-dss-interface



.. end-badges

* Free software: MIT license
* Documentation: https://py-dss-interface.readthedocs.io/en/latest/

The current py-dss-interface works only with Windows. The reason is that EPRI provides only Windows versions of OpenDSS. The package will work for Linux when EPRI releases the Linux version of OpenDSS.

The py-dss-interface package allows users to interact with OpenDSS using Python code, which can be particularly useful for automating tasks, performing simulations, and analyzing results. The package provides a range of functionality, including:

* Creating and modifying OpenDSS circuit models

* Running simulations and analyzing results

* Accessing and manipulating data within the circuit model

* Plotting results

The package is available on the Python Package Index (PyPI) and can be installed using pip, the Python package installer. OpenDSS does not have to be installed on the user's system to use the package, as the py-dss-interface provides an OpenDSS version.

Overall, the py-dss-interface is a powerful tool for anyone working with power distribution systems who wants to use Python for simulation and analysis.


Disclaimer
============
This Python Package is purely responsibility of Paulo Radatz and not his employer. Use this package at your own risk.

Installation
============

::

    pip install py-dss-interface

Examples
============
You can find several examples of Python scripts at this link: https://github.com/PauloRadatz/py-dss-interface-examples

Testing FPC Version
===================

The Free Pascal Compiler (FPC) may be used to support Linux and Mac OS X versions of the DLL interface. Only
64-bit interfaces are included. Efforts will be made to support the Progress Update, but not the Edit Form.

* The tests have been configured with an OpenDSS Version 8 repository at ``c:\src\OpenDSS\Version8``
* Use ``pytest -p no:faulthandler`` to run the test suite, using opendssdirect.dll within this py_dss_interface repository
* Use ``deploy_delphi`` to copy the Delphi-built DLL from the OpenDSS source tree into this repository for testing.

  * The test suite completes in 25-27 seconds on a 3-year-old laptop
  * 985/987 tests pass
  * In ``test_solution.py``, one test fails while interpreting an empty array from a call to ``bus_levels``
  * In ``test_monitors.py``, one test fails due to an incorrect continuation character in the byte stream

* Use ``deploy_fpc`` to copy the FPC-built DLL from the OpenDSS source tree into this repository for testing.

  * As with the Delphi build, the test suite completes in 25-27 seconds on a 3-year-old laptop
  * 983/987 tests pass
  * It was necessary to decrease the precision of floating-point comparison, i.e., the number of digits to the right of the decimal point, from 20 down to 10, 8, 5, or 4 in some tests. The lower precision levels generally correspond to calculated power or current levels, not per-unit values. This should be acceptable, pending further review.
  * As with the Delphi build, in ``test_solution.py``, one test fails while interpreting an empty array from a call to ``bus_levels``
  * As with the Delphi build, in ``test_monitors.py``, one test fails due to an incorrect continuation character in the byte stream
  * In ``test_lines.py``, an access violation occurs in ``read_yprim``
  * In ``test_solution.py``, the ``read_total_time`` often returns 0. In the FPC DLL, this function relies on ``GetTickCount64`, which may be less accurate than in the Delphi DLL.

* Use ``python Tom_PVSystem.py`` for a quicker test of new builds.

Thanks
=============
I want to thank Ênio Viana and Rodolfo Pilar Londero for all their contribution to the new version of the tool.


