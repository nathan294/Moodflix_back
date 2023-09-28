#!/bin/bash

cd /app

poetry install --with dev
poetry run pre-commit install -f --hook-type pre-commit
poetry run pre-commit autoupdate

echo "###### READY TO ROCK !"
sleep infinity