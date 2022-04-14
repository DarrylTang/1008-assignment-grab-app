import os.path
import sqlite3
from flask import Blueprint, render_template

# from flask_login import login_required, current_user
# from .models import Note
# from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")