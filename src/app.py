from os import getenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect


"""This module initializes app, loads secret key and implements CSRF protection."""

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
csrf = CSRFProtect(app)


import routes
