# app/main/routes.py

from . import main
from flask import render_template

@main.route('/')
def home():
    return render_template('home.html')
