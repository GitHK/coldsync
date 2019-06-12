# ColdSync

[![Build Status](https://travis-ci.org/GitHK/coldsync.svg?branch=master)](https://travis-ci.org/GitHK/coldsync)

Helps put important files into cold storage. For now `Google Cloud Storage` is supported.
The API is can be extend to add support other providers.

This project is build and released as a docker image with the scope of being 
as a sidecar container for application backup.

The image comes with `curl` and `kubectl`.
    
## Usage

To use the commands you must first setup the following environment variables:

- **CS_DATA_CENTER**  
- **CS_PROJECT_NAME**
- **CS_ENV_NAME** 
- **CS_GOOGLE_SERVICE_ACCOUNT_PATH**

Where **CS_DATA_CENTER**, **CS_PROJECT_NAME**, **CS_ENV_NAME** are used to identify the 
bucket in which files are stored.

The **CS_GOOGLE_SERVICE_ACCOUNT_PATH** must point to the google `credentials.json` file.


##### Show all files inside the bucket

    docker run --rm -i -t \
        -e CS_DATA_CENTER='central-europe' \
        -e CS_PROJECT_NAME='coold-data-storage' \
        -e CS_ENV_NAME='production' \
        -e CS_GOOGLE_SERVICE_ACCOUNT_PATH='/credentials.json' \
        -v $(pwd)/credentials.json:/credentials.json \
        coldsync coldsync list-files
        
##### Upload a file to the bucket

You may need to mount the file in the docker container in order to have access to it.

    docker run --rm -i -t \
        -e CS_DATA_CENTER='central-europe' \
        -e CS_PROJECT_NAME='coold-data-storage' \
        -e CS_ENV_NAME='production' \
        -e CS_GOOGLE_SERVICE_ACCOUNT_PATH='/credentials.json' \
        -v $(pwd)/credentials.json:/credentials.json \
        -v $(pwd)/sample.jpg:/sample.jpg \
        hubhk/coldsync coldsync upload-file /sample.jpg --remote_path 'thecat.jpg'

##### Download a file from the bucket

You may need to mount the download directory in the docker container in order to 
have access to the files which have been downloaded from your local file system.

    docker run --rm -i -t \
        -e CS_DATA_CENTER='central-europe' \
        -e CS_PROJECT_NAME='coold-data-storage' \
        -e CS_ENV_NAME='production' \
        -e CS_GOOGLE_SERVICE_ACCOUNT_PATH='/credentials.json' \
        -v $(pwd)/credentials.json:/credentials.json \
        -v $(pwd):/downloads \
        hubhk/coldsync coldsync download-file 'thecat.jpg' /downloads/thecat.jpg

##### Deleteing a file from the bucket

    docker run --rm -i -t \
        -e CS_DATA_CENTER='central-europe' \
        -e CS_PROJECT_NAME='coold-data-storage' \
        -e CS_ENV_NAME='production' \
        -e CS_GOOGLE_SERVICE_ACCOUNT_PATH='/credentials.json' \
        -v $(pwd)/credentials.json:/credentials.json \
        hubhk/coldsync coldsync delete-file 'thecat.jpg'


## Docker

Building image:

    docker build -t coldsync .

Running test:

    docker run --rm -i -t coldsync sh -c "pip install .[testing] && python setup.py test"