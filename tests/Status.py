import ctypes
import unittest

import Hash
from Error import Error

running = ctypes.c_bool()


class TestStatus(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.hash = Hash.load()

    def tearDown(self):
        """Call after every test case."""
        self.hash.HashTerminate()

    def testStatus(self):
        identifier = ctypes.c_size_t()
        b_path = ".".encode("utf-8")
        run_status = ctypes.c_bool()
        self.hash.HashInit()
        self.hash.HashDirectory(b_path, ctypes.byref(identifier))
        code: int = self.hash.HashStatus(identifier.value, ctypes.byref(run_status))
        while self.hash.HashStatus(identifier.value, ctypes.byref(running)) == 0 and running.value:
            pass
        self.hash.HashStop(identifier.value)
        self.assertEqual(Error.HASH_ERROR_OK, code,
                         f"Error code should be HASH_ERROR_OK {Error.HASH_ERROR_OK} but was {code}")
        self.assertTrue(run_status.value, "Status should be true")

    def testStatusErrorArgumentNull(self):
        self.hash.HashInit()
        code: int = self.hash.HashStatus(1, None)
        self.assertEqual(Error.HASH_ERROR_ARGUMENT_NULL, code,
                         f"Error code should be HASH_ERROR_ARGUMENT_NULL {Error.HASH_ERROR_ARGUMENT_NULL} but was {code}")

    def testErrorNotInitialized(self):
        code: int = self.hash.HashStatus(1, ctypes.byref(running))
        self.assertEqual(Error.HASH_ERROR_NOT_INITIALIZED, code,
                         f"Error code should be HASH_ERROR_NOT_INITIALIZED {Error.HASH_ERROR_NOT_INITIALIZED} but was {code}")

    # It is not clear how ARGUMENT_INVALID should look like
    # def testErrorInvalidArgument(self):
    #    self.hash.HashInit()
    #    code: int = self.hash.HashStatus(1, ctypes.byref(running))
    #    self.assertEqual(Error.HASH_ERROR_ARGUMENT_INVALID, code, f"Error code should be HASH_ERROR_ARGUMENT_INVALID {Error.HASH_ERROR_ARGUMENT_INVALID} but was {code}")


if __name__ == '__main__':
    unittest.main()  # run all tests
