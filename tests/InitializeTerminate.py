import unittest
import hash

class TestInitializeTerminate(unittest.TestCase):
    def setUp(self):
        """Call before every test case."""
        self.hash = hash.load()

    def tearDown(self):
        """Call after every test case."""
        self.hash.HashTerminate()

    def testInitializeError(self):
        self.hash.HashInit()
        code: int = self.hash.HashInit()
        self.assertEqual(8, code, f"Error code should be HASH_ERROR_ALREADY_INITIALIZED 8 but was {code}")

    def testTerminateError(self):
        code: int = self.hash.HashTerminate()
        self.assertEqual(7, code, f"Error code should be HASH_ERROR_NOT_INITIALIZED 7 but was {code}")

    def testInitialize(self):
        code: int = self.hash.HashInit()
        self.assertEqual(0, code, f"Error code should be HASH_ERROR_OK 0 but was {code}")

    def testTerminate(self):
        self.hash.HashInit()
        code: int = self.hash.HashTerminate()
        self.assertEqual(0, code, f"Error code should be HASH_ERROR_OK 0 but was {code}")

if __name__ == '__main__':
    unittest.main()  # run all tests
