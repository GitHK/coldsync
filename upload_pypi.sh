#!/bin/bash

# pip install twine   # optional
rm -rf dist
python setup.py sdist
twine upload dist/*