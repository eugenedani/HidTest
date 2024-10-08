import ctypes
import os
import time
import unittest

import CheckSum
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
        folder_name = "../libraries"
        b_path = folder_name.encode("utf-8")
        run_status = ctypes.c_bool()
        hash_content = ctypes.c_char_p()
        lines = []
        self.hash.HashInit()
        self.hash.HashDirectory(b_path, ctypes.byref(identifier))
        while self.hash.HashStatus(identifier.value, ctypes.byref(run_status)) == 0 and run_status.value:
            pass
        code: int = self.hash.HashReadNextLogLine(hash_content)
        lines.append(hash_content.value)
        self.hash.HashFree(hash_content)
        time.sleep(0.1)
        while self.hash.HashReadNextLogLine(hash_content) == 0:
            lines.append(hash_content.value)
            self.hash.HashFree(hash_content)
            time.sleep(0.1)
        self.hash.HashStop(identifier)
        self.assertEqual(Error.HASH_ERROR_OK.value, code, f"Error code should be {Error.HASH_ERROR_OK} but was {code}")
        self.check_content(folder_name, lines, identifier)

    def testLogEmptyFolder(self):
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
        self.assertEqual(Error.HASH_ERROR_LOG_EMPTY.value, code,
                         f"Error code should be {Error.HASH_ERROR_LOG_EMPTY} but was {code}")

    def testLogEmpty(self):
        identifier = ctypes.c_size_t()
        b_path = "../libraries/one".encode("utf-8")
        run_status = ctypes.c_bool()
        hash_content = ctypes.c_char_p()
        self.hash.HashInit()
        self.hash.HashDirectory(b_path, ctypes.byref(identifier))
        while self.hash.HashStatus(identifier.value, ctypes.byref(run_status)) == 0 and run_status.value:
            pass
        self.hash.HashReadNextLogLine(hash_content)
        code: int = self.hash.HashReadNextLogLine(hash_content)
        self.hash.HashStop(identifier)
        self.assertEqual(Error.HASH_ERROR_LOG_EMPTY.value, code,
                         f"Error code should be {Error.HASH_ERROR_LOG_EMPTY} but was {code}")

    def testReadErrorArgumentNull(self):
        self.hash.HashInit()
        code: int = self.hash.HashReadNextLogLine(None)
        self.assertEqual(Error.HASH_ERROR_ARGUMENT_NULL.value, code,
                         f"Error code should be {Error.HASH_ERROR_ARGUMENT_NULL} but was {code}")

    def testErrorNotInitialized(self):
        hash_content = ctypes.c_char_p()
        code: int = self.hash.HashReadNextLogLine(ctypes.byref(hash_content))
        self.assertEqual(Error.HASH_ERROR_NOT_INITIALIZED.value, code,
                         f"Error code should be {Error.HASH_ERROR_NOT_INITIALIZED} but was {code}")

    # It is not clear how ARGUMENT_INVALID should look like
    # def testErrorInvalidArgument(self):
    #    hash_content = ctypes.c_char_p()
    #    code: int = self.hash.HashReadNextLogLine(ctypes.byref(hash_content))
    #    self.assertEqual(Error.HASH_ERROR_ARGUMENT_INVALID.value, code, f"Error code should be {Error.HASH_ERROR_ARGUMENT_INVALID} but was {code}")

    def check_content(self, folder_name, lines, lib_id):
        files = []
        folder = os.scandir(folder_name)
        for entry in folder:
            if entry.is_file():
                files.append(entry)

        self.assertEqual(len(lines), len(files),
                         f"Hasl library found unexpected amount of files in {folder_name} folder")

        for i in range(len(lines) - 1):
            content: str = lines[i].decode("utf-8")
            values = content.split(" ")
            self.assertEqual(3, len(values), f"Line from Hash library has wrong format. File {files[i].name}")
            self.assertTrue(values[0].isdigit(),
                            f"Line from Hash library has wrong identifier: {values[0]} File {files[i].name} ")
            self.assertEqual(lib_id.value, int(values[0]),
                             f"Line from Hash library has wrong identifier. File {files[i].name}")
            self.assertIn(files[i].name, values[1], "Line from Hash library has wrong file name")
            md5 = CheckSum.CheckSum(files[i].path).md5()
            # It is not clear if md5 checksum should have capital letters or not capital letters
            # If it should have not capital letters then it is a bug because it has capital letters
            self.assertEqual(md5, values[2].lower(),
                             f"Line from Hash library has wrong MD5 checksum. File {files[i].name}")

if __name__ == '__main__':
    unittest.main()  # run all tests
