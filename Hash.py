import ctypes
import os


def load():
    hash_object = ctypes.cdll.LoadLibrary(os.path.normpath("C:/tasks/hid/test/libraries/hash.dll"))
    hash_object.HashDirectory.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)]
    hash_object.HashReadNextLogLine.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    hash_object.HashStatus.argtypes = [ctypes.c_size_t, ctypes.POINTER(ctypes.c_bool)]
    hash_object.HashStop.argtypes = [ctypes.c_size_t]
    hash_object.HashFree.argtypes = [ctypes.c_void_p]
    return hash_object
