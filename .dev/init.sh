#!/bin/bash

cd /app

poetry shell
poetry install --with dev --no-interaction
poetry run pre-commit install

echo "###### READY TO ROCK !"
sleep infinity