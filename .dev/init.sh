#!/bin/bash

cd /app/workspace

poetry install --with dev
# git init
# git config --global --add safe.directory /app/workspace
# poetry run pre-commit install -f --hook-type pre-commit
# poetry run pre-commit autoupdate

echo "###### READY TO ROCK !"
sleep infinity