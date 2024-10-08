import ctypes
import unittest

import Hash
from Error import Error

running = ctypes.c_bool()


class TestReadLine(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.hash = Hash.load()

    def tearDown(self):
        """Call after every test case."""
        self.hash.HashTerminate()

    def testReadLines(self):
        identifier = ctypes.c_size_t()
        b_path = "../libraries".encode("utf-8")
        run_status = ctypes.c_bool()
        hash_content = ctypes.c_char_p()
        self.hash.HashInit()
        self.hash.HashDirectory(b_path, ctypes.byref(identifier))
        while self.hash.HashStatus(identifier.value, ctypes.byref(run_status)) == 0 and run_status.value:
            pass
        code: int = self.hash.HashReadNextLogLine(hash_content)
        self.hash.HashStop(identifier)
        self.assertEqual({Error.HASH_ERROR_OK}, code,
                         f"Error code should be HASH_ERROR_LOG_EMPTY {Error.HASH_ERROR_OK} but was {code}")

    def testLogEmpty(self):
        identifier = ctypes.c_size_t()
        b_path = "../libraries/empty".encode("utf-8")
        run_status = ctypes.c_bool()
        hash_content = ctypes.c_char_p()
        self.hash.HashInit()
        self.hash.HashDirectory(b_path, ctypes.byref(identifier))
        while self.hash.HashStatus(identifier.value, ctypes.byref(run_status)) == 0 and run_status.value:
            pass
        code: int = self.hash.HashReadNextLogLine(hash_content)
        self.hash.HashStop(identifier)
        self.assertEqual({Error.HASH_ERROR_LOG_EMPTY}, code,
                         f"Error code should be HASH_ERROR_LOG_EMPTY {Error.HASH_ERROR_LOG_EMPTY} but was {code}")

    def testReadErrorArgumentNull(self):
        self.hash.HashInit()
        code: int = self.hash.HashReadNextLogLine(None)
        self.assertEqual(Error.HASH_ERROR_ARGUMENT_NULL, code,
                         f"Error code should be HASH_ERROR_ARGUMENT_NULL {Error.HASH_ERROR_ARGUMENT_NULL} but was {code}")

    def testErrorNotInitialized(self):
        hash_content = ctypes.c_char_p()
        code: int = self.hash.HashReadNextLogLine(ctypes.byref(hash_content))
        self.assertEqual(Error.HASH_ERROR_NOT_INITIALIZED, code,
                         f"Error code should be HASH_ERROR_NOT_INITIALIZED {Error.HASH_ERROR_NOT_INITIALIZED} but was {code}")

    # It is not clear how ARGUMENT_INVALID should look like
    # def testErrorInvalidArgument(self):
    #    hash_content = ctypes.c_char_p()
    #    code: int = self.hash.HashReadNextLogLine(ctypes.byref(hash_content))
    #    self.assertEqual(Error.HASH_ERROR_ARGUMENT_INVALID, code, f"Error code should be HASH_ERROR_ARGUMENT_INVALID {Error.HASH_ERROR_ARGUMENT_INVALID} but was {code}")


if __name__ == '__main__':
    unittest.main()  # run all tests
