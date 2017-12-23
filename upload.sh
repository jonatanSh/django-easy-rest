#!/usr/bin/env bash

# building
sudo python3 setup.py sdist

# uploading
python3 -m twine upload $(find dist/ -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")