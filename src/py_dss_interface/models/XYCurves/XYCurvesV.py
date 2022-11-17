# -*- encoding: utf-8 -*-
"""
 Created by eniocc at 11/10/2020
"""
import ctypes

from py_dss_interface.models import Bridge
from py_dss_interface.models.Base import Base
from py_dss_interface.models.Text.Text import Text
from py_dss_interface.models.XYCurves import XYCurves


class XYCurvesV(Base):
    """
    This interface can be used to read/write certain properties of the active DSS object.

    The structure of the interface is as follows:
        void XYCurvesS(int32_t Parameter, VARIANT *Argument);

    This interface returns a Variant with the result of the query according to the value of the variable Parameter,
    which can be one of the following.
    """

    def _x_array_read(self):
        """Gets the X values as a variant array of doubles. Set Npts to max number expected if setting."""
        return Bridge.var_array_function(self.dss_obj.XYCurvesV, ctypes.c_int(0), ctypes.c_int(0), None)

    def _x_array_write(self, argument):
        """Sets the X values as a variant array of doubles specified in Argument. Set Npts to max number expected
        if setting."""
        argument = Base.check_string_param(argument)
        t = Text(self.dss_obj)
        xyc = XYCurves.XYCurves(self.dss_obj)
        xyc_name = xyc.name # TODO
        return t.text(f'edit XYCurve.{xyc_name} Xarray = {argument}')

    def _y_array_read(self):
        """Gets the Y values as a variant array of doubles. Set Npts to max number expected if setting.."""
        return Bridge.var_array_function(self.dss_obj.XYCurvesV, ctypes.c_int(2), ctypes.c_int(0), None)

    def _y_array_write(self, argument):
        """Sets the Y values as a variant array of doubles specified in Argument. Set Npts to max number expected
        if setting."""
        argument = Base.check_string_param(argument)
        t = Text(self.dss_obj)
        xyc = XYCurves.XYCurves(self.dss_obj)
        xyc_name = xyc.name # TODO
        return t.text(f'edit XYCurve.{xyc_name} Yarray = {argument}')

        # variant_pointer = ctypes.pointer(automation.VARIANT())
        # variant_pointer.contents.value = argument
        # self.dss_obj.XYCurvesV(ctypes.c_int(3), variant_pointer)
        # return variant_pointer.contents.value
