# ColdSync

[![Build Status](https://travis-ci.org/GitHK/coldsync.svg?branch=master)](https://travis-ci.org/GitHK/coldsync)

Helps put important files into cold storage. For now `Google Cloud Storage` is supported.
The API is can be extend to add support other providers.

## Docker

Building image:

    docker build -t coldsync .

Running test:

    docker run --rm -i -t coldsync sh -c "pip install .[testing] && python setup.py test" 