#!/usr/bin/env bash

# removing old version
sudo pip3 uninstall django-easy-rest

# building current version
python3 setup.py sdist

# installing latest version
sudo pip3 install $(find dist/ -type f -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")