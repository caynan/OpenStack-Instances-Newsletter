#!venv/bin/python
from flask import Flask

APP = Flask(__name__)
from app import views
