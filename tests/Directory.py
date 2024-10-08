import ctypes
import os
import unittest

import hash

identifier = ctypes.c_size_t()

class TestDirectory(unittest.TestCase):

    def setUp(self):
       """Call before every test case."""
       self.hash = hash.load()

    def tearDown(self):
        """Call after every test case."""
        self.hash.HashStop(identifier.value)
        self.hash.HashTerminate()

    def testHashDirectory(self):
        b_path = ".".encode("utf-8")
        running = ctypes.c_bool()
        self.hash.HashInit()
        code: int = self.hash.HashDirectory(b_path, ctypes.byref(identifier))
        while self.hash.HashStatus(identifier.value, ctypes.byref(running)) == 0 and running.value:
          pass
        self.assertEqual(0, code, f"Error code should be HASH_ERROR_OK 0 but was {code}")

    def testDirErrorArgumentNull(self):
        self.hash.HashInit()
        code: int = self.hash.HashDirectory(None, ctypes.byref(identifier))
        self.assertEqual(6, code, f"Error code should be HASH_ERROR_ARGUMENT_NULL 6 but was {code}")

    def testIdErrorArgumentNull(self):
        self.hash.HashInit()
        code: int = self.hash.HashDirectory(".".encode("utf-8"), None)
        self.assertEqual(6, code, f"Error code should be HASH_ERROR_ARGUMENT_NULL 6 but was {code}")

    def testErrorNotInitialized(self):
        code: int = self.hash.HashDirectory(".".encode("utf-8"), ctypes.byref(identifier))
        self.assertEqual(7, code, f"Error code should be HASH_ERROR_NOT_INITIALIZED 7 but was {code}")

    # It is not clear how ARGUMENT_INVALID should look like
    #def testErrorInvalidArgument(self):
    #    self.hash.HashInit()
    #    code: int = self.hash.HashDirectory("wewerwerqweq".encode("utf-8"), ctypes.byref(identifier))
    #    self.assertEqual(5, code, f"Error code should be HASH_ERROR_ARGUMENT_INVALID 5 but was {code}")


if __name__ == '__main__':
    unittest.main()  # run all tests
