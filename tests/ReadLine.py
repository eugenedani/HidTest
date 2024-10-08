import ctypes
import unittest

import hash

running = ctypes.c_bool()

class TestReadLine(unittest.TestCase):

    def setUp(self):
        """Call before every test case."""
        self.hash = hash.load()

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
        self.assertEqual(0, code, f"Error code should be HASH_ERROR_OK 0 but was {code}")
        self.assertTrue(run_status.value, "Status should be true")

    def testStatusErrorArgumentNull(self):
        self.hash.HashInit()
        code: int = self.hash.HashStatus(1, None)
        self.assertEqual(6, code, f"Error code should be HASH_ERROR_ARGUMENT_NULL 6 but was {code}")

    def testErrorNotInitialized(self):
        code: int = self.hash.HashStatus(1, ctypes.byref(running))
        self.assertEqual(7, code, f"Error code should be HASH_ERROR_NOT_INITIALIZED 7 but was {code}")

    # It is not clear how ARGUMENT_INVALID should look like
    # def testErrorInvalidArgument(self):
    #    self.hash.HashInit()
    #    code: int = self.hash.HashStatus(1, ctypes.byref(running))
    #    self.assertEqual(5, code, f"Error code should be HASH_ERROR_ARGUMENT_INVALID 5 but was {code}")


if __name__ == '__main__':
    unittest.main()  # run all tests
