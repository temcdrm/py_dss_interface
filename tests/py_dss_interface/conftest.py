# -*- coding: utf-8 -*-
# @Time    : 6/4/2021 7:45 AM
# @Author  : Paulo Radatz
# @Email   : paulo.radatz@gmail.com
# @File    : conftest.py
# @Software: PyCharm

import os
import pathlib

import pytest

import py_dss_interface

script_path = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='function')
def solve_snap_13bus():
    dss = py_dss_interface.DSSDLL()
    actual = dss.started
    # expected = True

    # message = f"OpenDSSDirectDLL has been loaded: {actual}"

    # assert actual is expected, message

    dss.text("set DefaultBaseFrequency=60")
    dss13_path = os.path.join(pathlib.Path(script_path), "cases", "13Bus", "IEEE13Nodeckt.dss")
    dss.text(f"compile {dss13_path}")

    dss.dss_write_allow_forms(0)
    return dss

# @pytest.fixture(autouse=True)
# def slow_down_tests():
#     yield
#     time.sleep(1)
