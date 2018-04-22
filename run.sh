#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

source .venv/bin/activate

FLASK_APP=server.py flask run
