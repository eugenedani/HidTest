import ctypes
import time
import unittest

import Hash
from Error import Error

running = ctypes.c_bool()


class TestStop(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.hash = Hash.load()

    def tearDown(self):
        """Call after every test case."""
        self.hash.HashTerminate()

    def testStop(self):
        identifier = ctypes.c_size_t()
        b_path = ".".encode("utf-8")
        run_status = ctypes.c_bool()
        hash_content = ctypes.c_char_p()
        self.hash.HashInit()
        self.hash.HashDirectory(b_path, ctypes.byref(identifier))
        self.hash.HashStatus(identifier.value, ctypes.byref(run_status))
        while self.hash.HashStatus(identifier.value, ctypes.byref(running)) == 0 and running.value:
            pass
        while self.hash.HashReadNextLogLine(hash_content) == 0:
            self.hash.HashFree(hash_content)
            time.sleep(0.1)
        code: int = self.hash.HashStop(identifier.value)
        self.assertEqual(Error.HASH_ERROR_OK.value, code, f"Error code should be {Error.HASH_ERROR_OK} but was {code}")

    def testErrorNotInitialized(self):
        code: int = self.hash.HashStop(0)
        self.assertEqual(Error.HASH_ERROR_NOT_INITIALIZED.value, code,
                         f"Error code should be {Error.HASH_ERROR_NOT_INITIALIZED} but was {code}")

    def testErrorInvalidArgument(self):
        self.hash.HashInit()
        code: int = self.hash.HashStop(1)
        self.assertEqual(Error.HASH_ERROR_ARGUMENT_INVALID.value, code,
                         f"Error code should be {Error.HASH_ERROR_ARGUMENT_INVALID} but was {code}")


if __name__ == '__main__':
    unittest.main()  # run all tests
