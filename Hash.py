import ctypes
import os


def load():
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, 'libraries\hash.dll')
    hash_object = ctypes.cdll.LoadLibrary(file_path)
    hash_object.HashDirectory.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)]
    hash_object.HashReadNextLogLine.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    hash_object.HashStatus.argtypes = [ctypes.c_size_t, ctypes.POINTER(ctypes.c_bool)]
    hash_object.HashStop.argtypes = [ctypes.c_size_t]
    hash_object.HashFree.argtypes = [ctypes.c_void_p]
    return hash_object
