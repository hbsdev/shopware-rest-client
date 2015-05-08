#!/bin/bash
set -e # This will cause the shell to exit immediately if a simple command exits with a nonzero exit value
source ./secret
./pytest-genscript.sh
python setup.py test
python setup.py sdist --format zip
