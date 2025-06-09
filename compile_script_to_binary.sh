#!/bin/bash

source .venv/bin/activate
python -m nuitka --remove-output --enable-plugin=pylint-warnings --onefile archive_all_folders_in_directory.py
