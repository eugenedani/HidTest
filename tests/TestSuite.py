import unittest

import tests.Directory
import tests.Free
import tests.InitializeTerminate
import tests.ReadLine
import tests.Status
import tests.Stop


def suite():
    loader = unittest.TestLoader()
    hash_suite = unittest.TestSuite()
    hash_suite.addTest(loader.loadTestsFromModule(tests.InitializeTerminate))
    hash_suite.addTest(loader.loadTestsFromModule(tests.ReadLine))
    hash_suite.addTest(loader.loadTestsFromModule(tests.Directory))
    hash_suite.addTest(loader.loadTestsFromModule(tests.Status))
    hash_suite.addTest(loader.loadTestsFromModule(tests.Stop))
    hash_suite.addTest(loader.loadTestsFromModule(tests.Free))
    return hash_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
