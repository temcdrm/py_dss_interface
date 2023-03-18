# -*- encoding: utf-8 -*-
"""
 Created by eniocc at 11/10/2020
"""
import ctypes

from py_dss_interface.models.Base import Base


class VSourcesS(Base):
    """
    This interface can be used to read/write certain properties of the active DSS object.

    The structure of the interface is as follows:
        CStr VSourcesS(int32_t Parameter, CStr Argument);

    This interface returns a string with the result of the query according to the value of the variable Parameter,
    which can be one of the following.
    """

    def _name_read(self):
        result = ctypes.c_char_p(self._dss_obj.VsourcesS(ctypes.c_int32(0), ctypes.c_int32(0)))
        return result.value.decode('ascii')

    def _name_write(self, argument):
        argument = Base._check_string_param(argument)
        result = ctypes.c_char_p(self._dss_obj.VsourcesS(ctypes.c_int32(1), argument.encode('ascii')))
        return result.value.decode('ascii')
