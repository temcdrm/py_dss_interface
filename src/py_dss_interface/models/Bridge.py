# -*- encoding: utf-8 -*-
"""
 Created by eniocc at 30/04/2021
"""
import ctypes
import logging
import struct
import sys
from enum import Enum
from typing import List, Union

import numpy as np
if sys.platform == 'win32':
    try:
        from comtypes import automation
    except:
        print('\nCOM automation is not supported on this platform.\nvariant_pointer_read and variant_pointer_write functions will not work.\n')


logger = logging.getLogger('opendssdirect.core')


def is_x64() -> bool:
    """
    Returns True if the system is 64-bit, False otherwise.
    """
    return struct.calcsize("P") == 8


def is_windows() -> bool:
    """
    Returns True if the system is running Delphi (or FPC) on Windows, False otherwise.
    """
    return 'darwin' not in sys.platform and 'linux' not in sys.platform


POINTER = ctypes.c_int64 if is_x64() else ctypes.c_int32
HEADER_SIZE = 4 if is_windows() else 8


class VArg(ctypes.Structure):
    _fields_ = [
        ('dtype', ctypes.c_uint64),
        ('p', ctypes.POINTER(None)),
        ('dum1', ctypes.c_uint64),
        ('dum2', ctypes.c_uint64),
    ]


class VarArray(ctypes.Structure):
    _fields_ = [
        ('dimcount', ctypes.c_uint8),
        ('flags', ctypes.c_uint8),
        ('elementsize', ctypes.c_uint32),
        ('lockcount', ctypes.c_uint32),
        ('data', ctypes.POINTER(None)),
        ('length', ctypes.c_uint),
        ('lbound', ctypes.c_uint),
    ]


def c_types_function(f: callable, param: Union[int, str], dss_arg: Union[bytes, str], name: str) -> str:
    """
    Calls the given ctypes function with the given parameters, and returns the result as a string.
    """
    if isinstance(dss_arg, str):
        dss_arg = dss_arg.encode('ascii')

    logger.debug(f"Calling function {name} with arguments {(param, dss_arg)}")
    r = f(param, dss_arg)

    if isinstance(r, bytes):
        r = r.decode('ascii')
    return r


def variant_pointer_read(f: callable, param: int, optional=None) -> List:
    """
    Reads a COM variant pointer and returns its value as a list.
    """
    variant_pointer = ctypes.pointer(automation.VARIANT())
    if optional:
        f(ctypes.c_int(param), variant_pointer, optional)
    else:
        f(ctypes.c_int(param), variant_pointer)

    r = list(variant_pointer.contents.value)
    while None in r:
        r.remove(None)
    return r

def pointer_read(f: callable, param: int, optional=None) -> List:
    f.argtypes = [
    ctypes.c_long,
    ctypes.POINTER(ctypes.c_void_p),
    ctypes.POINTER(ctypes.c_long),
    ctypes.POINTER(ctypes.c_long)
    ]

    f.restype = None

    myPointer = ctypes.c_void_p()  # Create a pointer variable
    myType = ctypes.c_long()
    mySize = ctypes.c_long()

    if optional:
        op_list = [optional]
        c_array = (ctypes.c_int32 * len(op_list))(*op_list)
        myPointer = ctypes.cast(c_array, ctypes.c_void_p)

        f(param, ctypes.byref(myPointer), ctypes.byref(myType), ctypes.byref(mySize))
    else:
        f(
        param,
        ctypes.byref(myPointer),
        ctypes.byref(myType),
        ctypes.byref(mySize)
    )

    # 0 - Boolean, 1- Integer (32 bit), 2- double (64 bit), 3- Complex, 4- String, 5-byte stream.
    num_type = 0
    if myType.value == 1:
        c_type = ctypes.c_int32
        num_type = 4
    elif myType.value == 2:
        c_type = ctypes.c_double
        num_type = 8
    elif myType.value == 3:
        c_type = ctypes.c_double
        num_type = 8
    elif myType.value == 4:  # string
        c_type = ctypes.c_char
        num_type = 1
    elif myType.value == 5:  # byte stream
        c_type = ctypes.c_char
        num_type = 1
    # Access the returned array
    array_length = int(mySize.value / num_type)
    # data_array = ctypes.cast(myPointer, ctypes.POINTER(ctypes.c_int * array_length)).contents

    if not bool(myPointer):
        return []
    data_array = ctypes.cast(myPointer, ctypes.POINTER(c_type * array_length)).contents

    # Convert the data_array to a Python list
    if myType.value == 4:
        python_list = list(data_array.raw.decode('utf-8').replace('\x00', '__SPLITHERE__').split('__SPLITHERE__')[:])
        while "" in python_list:
            python_list.remove("")
    else:
        python_list = list(data_array)
    # Access the returned values
    # print(f"Data array: {python_list}")
    # print(f"myType: {myType.value}")
    # print(f"mySize: {mySize.value}")

    return python_list

def pointer_write(f: callable, param: int, arg: List, myType):
    """
    Writes a list to a COM variant pointer.
    """

    mode = param
    f.argtypes = [
        ctypes.c_long,
        ctypes.POINTER(ctypes.c_void_p),
        ctypes.POINTER(ctypes.c_long),
        ctypes.POINTER(ctypes.c_long)
    ]

    f.restype = None

    if myType == 1:
        c_type = ctypes.c_int32
    elif myType == 2:
        c_type = ctypes.c_double
    elif myType == 3:
        c_type = ctypes.c_double
    elif myType == 4:
        c_type = ctypes.c_char

    # Prepare input values
    data = arg

    c_array = (c_type * len(data))(*data)
    my_type = ctypes.c_long(myType)
    my_size = ctypes.c_long(len(data))
    pc_array = ctypes.cast(c_array, ctypes.c_void_p)
    f(mode, ctypes.byref(pc_array), ctypes.byref(my_type), ctypes.byref(my_size))

    # elif myType.value == 2:
    #     c_type = ctypes.c_double
    #     num_type = 8

    # c_array = (ctypes.c_void_p * len(data))(*data)
    # c_array = ctypes.c_int

    # Declare variables for the procedure parameters
    # my_pointer = ctypes.
    # my_type = ctypes.c_long(1)


    # n1 = ctypes.c_int32(2)
    # n = ctypes.POINTER(ctypes.byref(c_array))

    # Update the pointer value with the C array
    # ctypes.memmove(my_pointer, c_array, len(c_array) * ctypes.sizeof(ctypes.c_long))

    # Call the procedure
    # f(mode, ctypes.byref(c_array), ctypes.byref(my_type), ctypes.byref(my_size))
    # ctypes.cast(c_array, ctypes.c_void_p)
    # ctypes.cast(n, ctypes.c_void_p)
    # pc_array = ctypes.cast(c_array, ctypes.POINTER(ctypes.c_void_p))




    # Access the returned values
    # print(f"Data array: {python_list}")
    # print(f"myType: {my_type.value}")
    # print(f"mySize: {my_size.value}")

def variant_pointer_write(f: callable, param: int, arg: List) -> Union[List, int]:
    """
    Writes a list to a COM variant pointer.
    """
    variant_pointer = ctypes.pointer(automation.VARIANT())
    variant_pointer.contents.value = arg
    f(ctypes.c_int(param), variant_pointer)

    r = variant_pointer.contents.value

    if isinstance(r, int):
        return r
    else:
        return list(variant_pointer.contents.value)


class DataType(Enum):
    Unknown = 0
    CString = 0x2008
    Float64 = 0x2005
    Int32 = 0x2003
    ByteStream = 0x2011


def cast_array(var_arr, dtype):
    if dtype == DataType.CString:
        data = ctypes.cast(var_arr.data, ctypes.POINTER(ctypes.c_void_p))
        return [
            ctypes.cast(s, ctypes.c_char_p).value.decode('utf-8')
            for s in data.contents[:var_arr.length]
            if s != 0
        ]
    elif dtype == DataType.Float64:
        data = ctypes.cast(var_arr.data, ctypes.POINTER(ctypes.c_double))
        return np.frombuffer(data.contents, count=var_arr.length)
    elif dtype == DataType.Int32:
        data = ctypes.cast(var_arr.data, ctypes.POINTER(ctypes.c_int32))
        return np.frombuffer(data.contents, count=var_arr.length)
    elif dtype != DataType.ByteStream:
        raise ValueError(f"Unsupported dtype {dtype}")


def process_var_array(var_arr, dtype):
    """Process a VarArray object and convert it to a list of values.

    Args:
        var_arr: A VarArray object to process.
        dtype: The data type of the VarArray object.

    Returns:
        A list of values extracted from the VarArray object.
    """
    if var_arr.length == 0:
        return []  # or None, depending on the desired behavior

    result = cast_array(var_arr, dtype)

    if dtype == DataType.CString:
        result = [s for s in result if s.lower() != 'none']

    return result


def process_var(varg, name):
    """Process a Var object and convert it to a list of values.

    Args:
        varg: A Var object to process.
        name: The name of the Var object.

    Returns:
        A list of values extracted from the Var object.
    """
    data_types = {
        DataType.CString: process_var_array,
        DataType.Float64: process_var_array,
        DataType.Int32: process_var_array,
        DataType.ByteStream: process_var_array,  # TODO: implement DataFrame creation
    }

    data_type = varg.dtype
    processing_func = data_types.get(data_type)

    if processing_func is None:
        raise ValueError(f"Unsupported dtype {data_type} returned for {name}. Please contact developer")

    return processing_func(varg.p.contents, data_type)


def var_array_function(f, param, optional, name):
    varg = VArg(0, None, 0, 0)
    p = ctypes.POINTER(VArg)(varg)
    if optional is not None:
        f(param, p, optional)
    else:
        logger.debug(f"Calling function {name} with arguments {(param, p)}")
        f(param, p)

    logger.debug(f"Successively called and returned from function {name}")
    # var_arr = ctypes.cast(varg.p, ctypes.POINTER(VarArray)).contents

    return process_var(varg, name)

class MyComplex(ctypes.Structure):
    _fields_ = [("re", ctypes.c_double),
                ("im", ctypes.c_double)]
