import ctypes
import os
import sys


def load():
    dll_name = "hash.{:s}".format("dll" if sys.platform[:3].lower() == "win" else "so")
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, 'libraries\{:s}'.format(dll_name))
    hash_object = ctypes.CDLL(file_path)
    hash_object.HashDirectory.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_size_t)]
    hash_object.HashReadNextLogLine.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    hash_object.HashStatus.argtypes = [ctypes.c_size_t, ctypes.POINTER(ctypes.c_bool)]
    hash_object.HashStop.argtypes = [ctypes.c_size_t]
    hash_object.HashFree.argtypes = [ctypes.c_void_p]
    return hash_object


# I'm not sure if it is correct implementation, but it works on windows
def unload(dll):
    handle = dll._handle
    del dll
    if sys.platform[:3].lower() == "win":
        ctypes.windll.kernel32.FreeLibrary(handle)
    # else:
    #  code for another OS
