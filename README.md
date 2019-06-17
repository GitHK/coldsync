# coldsync

[![Build Status](https://travis-ci.org/GitHK/coldsync.svg?branch=master)](https://travis-ci.org/GitHK/coldsync)
[![Python 3.4](https://img.shields.io/badge/python-3.4-blue.svg)](https://www.python.org/downloads/release/python-340/)
[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Pypy 3.5](https://img.shields.io/badge/pypy-3.5-blue.svg)](http://doc.pypy.org/en/latest/release-v7.0.0.html)

Backup important files to cold storage.

    pip install coldsync

`Google Cloud Storage` is supported for now. The API is can be extend to add support other providers. Inside the storage module extend the `BaseStorage` 
to add support for other providers.

    
## Usage

To use the commands you must first setup the following environment variables:

- **CS_DATA_CENTER**  
- **CS_PROJECT_NAME**
- **CS_ENV_NAME** 
- **CS_GOOGLE_SERVICE_ACCOUNT_PATH**

Where **CS_DATA_CENTER**, **CS_PROJECT_NAME**, **CS_ENV_NAME** are used to identify the 
bucket in which files are stored.

The **CS_GOOGLE_SERVICE_ACCOUNT_PATH** must point to your google `credentials.json` file.

## Examples

**Show all files inside the bucket**

    CS_DATA_CENTER='central-europe' \
    CS_PROJECT_NAME='coold-data-storage' \
    CS_ENV_NAME='production' \
    CS_GOOGLE_SERVICE_ACCOUNT_PATH='credentials.json' \
    coldsync list-files
        
**Upload a file to the bucket**

You may need to mount the file in the docker container in order to have access to it.

    CS_DATA_CENTER='central-europe' \
    CS_PROJECT_NAME='coold-data-storage' \
    CS_ENV_NAME='production' \
    CS_GOOGLE_SERVICE_ACCOUNT_PATH='credentials.json' \
    coldsync upload-file sample.jpg --remote_path 'thecat.jpg'

**Download a file from the bucket**

You may need to mount the download directory in the docker container in order to 
have access to the files which have been downloaded from your local file system.

    CS_DATA_CENTER='central-europe' \
    CS_PROJECT_NAME='coold-data-storage' \
    CS_ENV_NAME='production' \
    CS_GOOGLE_SERVICE_ACCOUNT_PATH='credentials.json' \
    coldsync download-file 'thecat.jpg' thecat.jpg

**Deleting a file from the bucket**

    CS_DATA_CENTER='central-europe' \
    CS_PROJECT_NAME='coold-data-storage' \
    CS_ENV_NAME='production' \
    CS_GOOGLE_SERVICE_ACCOUNT_PATH='credentials.json' \
    coldsync delete-file 'thecat.jpg'

## Tests

Running test suite
    
    python setup.py test