#!/bin/bash
set -e # This will cause the shell to exit immediately if a simple command exits with a nonzero exit value

# remove all python cache files:
find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf

source ./secret
./pytest-genscript.sh
python setup.py test
python setup.py sdist --format zip
