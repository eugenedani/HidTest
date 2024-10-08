import unittest

import Hash
from Error import Error


class TestInitializeTerminate(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.hash = Hash.load()

    def tearDown(self):
        """Call after every test case."""
        self.hash.HashTerminate()

    def testInitializeError(self):
        self.hash.HashInit()
        code: int = self.hash.HashInit()
        self.assertEqual(Error.HASH_ERROR_ALREADY_INITIALIZED, code,
                         f"Error code should be {Error.HASH_ERROR_ALREADY_INITIALIZED} 8 but was {code}")

    def testTerminateError(self):
        code: int = self.hash.HashTerminate()
        self.assertEqual(Error.HASH_ERROR_NOT_INITIALIZED, code,
                         f"Error code should be HASH_ERROR_NOT_INITIALIZED {Error.HASH_ERROR_NOT_INITIALIZED} but was {code}")

    def testInitialize(self):
        code: int = self.hash.HashInit()
        self.assertEqual(Error.HASH_ERROR_OK, code,
                         f"Error code should be HASH_ERROR_OK {Error.HASH_ERROR_OK} but was {code}")

    def testTerminate(self):
        self.hash.HashInit()
        code: int = self.hash.HashTerminate()
        self.assertEqual(Error.HASH_ERROR_OK, code,
                         f"Error code should be HASH_ERROR_OK {Error.HASH_ERROR_OK} but was {code}")


if __name__ == '__main__':
    unittest.main()  # run all tests
