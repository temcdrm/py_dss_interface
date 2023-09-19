# -*- coding: utf-8 -*-
# @Time    : 9/19/2023 8:47 AM
# @Author  : Paulo Radatz
# @Email   : pradatz@epri.com
# @File    : Tom_PVSystem.py
# @Software: PyCharm

import py_dss_interface
import pathlib
import os

# Using the OpenDSS repository
dss = py_dss_interface.DSS("C:\src\OpenDSS\Version8\Source")
dss = py_dss_interface.DSS()

dss.text("set DefaultBaseFrequency=60")
script_path = os.path.dirname(os.path.abspath(__file__))
dss13_path = os.path.join(pathlib.Path(script_path), "tests", "py_dss_interface", "cases", "13Bus", "IEEE13Nodeckt.dss")
dss.text(f"compile {dss13_path}")

dss.text(r"New XYCurve.MyPvsT npts=4  xarray=[0  25  75  100]  yarray=[1 1 1 1]")
dss.text(r"New XYCurve.MyEff npts=4  xarray=[.1  .2  .4  1.0]  yarray=[1 1 1 1]")
dss.text(r"New PVSystem.PV1 phases=3 "
         r"bus1=680 "
         r"kV=4.16  "
         r"kVA=600  "
         r"irrad=1  "
         r"Pmpp=500 "
         r"temperature=25 "
         r"PF=1 "
         r"%cutin=0.1 "
         r"%cutout=0.1  "
         r"effcurve=Myeff  "
         r"P-TCurve=MyPvsT")

dss.text("solve")

print(dss.pvsystems.names)
