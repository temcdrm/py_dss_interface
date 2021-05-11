# -*- encoding: utf-8 -*-
"""
 Created by eniocc at 11/10/2020
"""
import ctypes
from py_dss_interface.models.Base import Base


class CircuitF(Base):
    """
    This interface can be used to read/write certain properties of the active DSS object.

    The structure of the interface is as follows:
        double CircuitF(int32_t Parameter, double Argument1, double Argument2);

    This interface returns a floating point number (IEEE754 64 bits) according to the number sent in the variable
    “parameter”. The parameter can be one of the following.
    """

    def circuit_float(self, first, second) -> float:
        return float(self.dss_obj.CircuitF(ctypes.c_int32(first), ctypes.c_double(second)))

    def circuit_capacity(self) -> float:
        """Returns the total capacity of the active circuit. Or this parameter it is necessary to specify the start
        and increment of the capacity in the arguments argument1 and argument2 respectively. """
        return self.circuit_float(0, 0)
