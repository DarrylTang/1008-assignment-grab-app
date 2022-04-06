import os.path
import sqlite3
from flask import Blueprint, render_template

# from flask_login import login_required, current_user
# from .models import Note
# from . import db

views = Blueprint('views', __name__)


# @views.route('/')
# def home():
#     return render_template("home.html")

# @views.route('/map')
# def map():
#     return render_template("home.html")

# @views.route('/test')
# def test():
#     return render_template("test.html")


@views.route('/review')
def review1():
    # amended for reviews
    # tutorial: https://www.youtube.com/watch?v=8wKsyGtPo3I
    # https://stackoverflow.com/questions/28126140/python-sqlite3-operationalerror-no-such-table
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "drivers.db")
    # connect = sqlite3.connect("drivers.db")
    connect = sqlite3.connect(db_path)
    connect.row_factory = sqlite3.Row
    cur = connect.cursor()
    cur.execute("SELECT * FROM driversTable")
    rows = cur.fetchall()
    return render_template("review.html", rows=rows)


@views.route('/review2')
def review2():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "sortDriverRating.db")
    # connect = sqlite3.connect("drivers.db")
    connect = sqlite3.connect(db_path)
    connect.row_factory = sqlite3.Row
    cur = connect.cursor()
    cur.execute("SELECT * FROM sortedDriverRatingTable")
    newRows = cur.fetchall()
    return render_template("review.html", rows=newRows)


@views.route('/driver_detail')
def driver_detail():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "drivers.db")
    # connect = sqlite3.connect("drivers.db")
    connect = sqlite3.connect(db_path)
    connect.row_factory = sqlite3.Row
    cur = connect.cursor()
    cur.execute("SELECT * FROM driversTable")
    newRows = cur.fetchall()
    return render_template("driver_detail.html", rows=newRows)

# @views.route('/driver_detail/<int:driverId>')
# def driver_detail(driverId):
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     db_path = os.path.join(BASE_DIR, "drivers.db")
#     # connect = sqlite3.connect("drivers.db")
#     connect = sqlite3.connect(db_path)
#     connect.row_factory = sqlite3.Row
#     cur = connect.cursor()
#     cur.execute("SELECT * FROM driversTable WHERE driverId = driverId")
#     rows = cur.fetchall()
#     return render_template("driver_detail.html", row=driverId)

# @views.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         note = request.form.get('note')
#         if len(note) < 1:
#             flash('Note is too short!', category='error')
#         else:
#             new_note = Note(data=note, user_id=current_user.id)
#             db.session.add(new_note)
#             db.session.commit()
#             flash('Note added!', category='success')
#     return render_template("home.html", user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commmit()
#     return jsonify({})
#
# @views.route('/account')
# @login_required
# def account():
#     return render_template("account.html")
