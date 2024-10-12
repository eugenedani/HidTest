## Bug report

I did not commit hash.dll and hash.lib to HitHub they should be in libraries folder.
I use Python project environment and project Python interpreter
python -m venv hid
venv\Scripts\activate

### Environment

Tests were run on Windows 10 Pro build 19045.4957 (64 bit)
Python 3.11 (32 bit)

### 1 HashInit method the second call in a row issue

#### Steps to Reproduce

1. call HashInit() method
2. call HashInit() method again

### Expected Result

Return code of the method is HASH_ERROR_ALREADY_INITIALIZED 8

### Actual Result

Return code of the method is HASH_ERROR_OK 0

### Severity/Priority

Medium

___

### 2 HashStop method "not initialized" issue

#### Steps to Reproduce

1. call HashStop(0) method as the first calling method before HashInit() method calling

### Expected Result

Return code of the method is HASH_ERROR_NOT_INITIALIZED 7

### Actual Result

Return code of the method is HASH_ERROR_ARGUMENT_INVALID 5

### Severity/Priority

Medium

___

### 3 HashFree does not have return codes

Behaviour of HashFree is confused. According to specification it does not have any return codes.
But it returns some ones. I suppose it has some codes in order to have information from the method, but they are not
described

#### Steps to Reproduce

1. Use header file hash.h as a specification

### Expected Result

Method returns codes and they are described in specification

### Actual Result

    /**
     * @brief Release memory allocated by functions in this library
     * 
     * @param hash [in] Memory to release
     */
    EXPORT
    void HashFree(void* hash);

### Severity/Priority

Critical

---

### 4 HashReadNextLogLine returns wrong empty code

#### Steps to Reproduce

1. Use directory with one file
2. Call

            HashInit();
            HashDirectory(path_to_one_file_folder, &identifier);
            while self.hash.HashStatus(identifier, &run_status) == 0 && run_status.value;
            HashReadNextLogLine(&hash_content)
            code = HashReadNextLogLine(&hash_content)

### Expected Result

Return code of the method is HASH_ERROR_LOG_EMPTY 4

### Actual Result

Return code of the method is HASH_ERROR_GENERAL 1

### Severity/Priority

Medium

---

### 5 HashReadNextLogLine returns wrong empty code for empty folder

#### Steps to Reproduce

1. Use directory without files
2. Call

         HashInit();
         HashDirectory(path_to_empty_folder, &identifier);
         while HashStatus(identifier, &run_status) == 0 && run_status;
         code = HashReadNextLogLine(&hash_content);

### Expected Result

Return code of the method is HASH_ERROR_LOG_EMPTY 4

### Actual Result

Return code of the method is HASH_ERROR_GENERAL 1

### Severity/Priority

Medium

___

### 6 HashDirectory or HashReadNextLogLine returns wrong MD5 checksum

#### Steps to Reproduce

1. Use directory 2 files (hash.dll and hash.lib)
2. Call

         HashInit();
         HashDirectory(path_to_2_files_folder, &identifier);
         while HashStatus(identifier, &run_status) == 0 && run_status;
         while HashReadNextLogLine(&line) == 0:
         {   
           std::cout << line << std::endl;
           HashFree(line);
           std::this_thread::sleep_for(std::chrono::milliseconds(100));
         }
        HashStop(identifier)
        HashTerminate()

### Expected Result

hash.lib has MD5 = 722b232def0d4e31157bc4549ecc1594

### Actual Result

hash.lib has MD5 = 722b232defd4e31157bc4549ecc1594

### Severity/Priority

Critical

___

### 7 HashTerminate did not clean hash

I'm not sure if it is an issue or not. It is not clear from description, but I have added it here just in case

#### Steps to Reproduce

1. Use directory 2 files (hash.dll and hash.lib)
2. Call

         HashInit();
         HashDirectory(path_to_2_files_folder, &identifier);
         while HashStatus(identifier, &run_status) == 0 && run_status;
         while HashReadNextLogLine(&line) == 0:
         {   
           std::cout << line << std::endl;
           std::this_thread::sleep_for(std::chrono::milliseconds(100));
         }
        HashStop(identifier)
        HashTerminate()
3. Call the same code in a row in one file

### Expected Result

the second attempt will have 2 files

### Actual Result

the second attempt has 4 files

### Severity/Priority

Critical
