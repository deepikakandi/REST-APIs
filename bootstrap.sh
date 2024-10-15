#!/bin/sh
export FLASK_APP=./flask-project/app.py
pipenv run flask --debug run -h 0.0.0.0