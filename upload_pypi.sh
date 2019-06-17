#!/bin/bash

# pip install twine   # optional
python setup.py sdist
twine upload dist/*