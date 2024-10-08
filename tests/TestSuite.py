import unittest
import tests.InitializeTerminate
import tests.Directory
import tests.Status
import tests.ReadLine



def suite():
    loader = unittest.TestLoader()
    hash_suite = unittest.TestSuite()
    hash_suite.addTest(loader.loadTestsFromModule(tests.InitializeTerminate))
    hash_suite.addTest(loader.loadTestsFromModule(tests.Directory))
    hash_suite.addTest(loader.loadTestsFromModule(tests.Status))
    hash_suite.addTest(loader.loadTestsFromModule(tests.ReadLine))
    return hash_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
