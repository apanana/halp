#!/bin/bash

# Clean up our pycache 
# Taken from: https://stackoverflow.com/questions/28991015/python3-project-remove-pycache-folders-and-pyc-files/41386937
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

# Run our tests
python setup.py test