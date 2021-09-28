#!/bin/sh

pytest -s -vvv . && black --check --diff . && isort --check-only --diff . && mypy . && flake8 .
