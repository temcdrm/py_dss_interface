# -*- encoding: utf-8 -*-
"""
 Created by eniocc at 11/10/2020
"""
from py_dss_interface.models.Base import Base


class ActiveClassS(Base):
    """
    This interface can be used to read/modify the properties of the ActiveClass Class where the values are strings.

    The structure of the interface is as follows:
        CStr ActiveClassI(int32_t Parameter, CStr argument)

    This interface returns a string, the first parameter is used to specify the property of the class to be used
    and the second parameter can be used to modify the value of the property when necessary. Reading and writing
    properties are separated and require a different parameter number to be executed.

    The properties (parameter) are integer numbers and are described as follows.
    """

    def active_class_get_name(self) -> str:
        """Gets the name of the active Element of the Active class."""
        return self.dss_obj.get_string(0, 0)

    def active_class_write_name(self, argument) -> str:
        """Sets the name of the active Element of the Active class.
        : TODO: After sets the name what is the return type? str or int? How can I treat this? >=0 is ok?
        """
        return self.dss_obj.get_string(1, argument)

    def active_class_set_name(self) -> str:
        """Sets the name of the active Element of the Active class.
         TODO: After sets the name what is the return type? str or int? How can I treat this? >=0 is ok?
         """
        return self.dss_obj.get_string(2, 0)
