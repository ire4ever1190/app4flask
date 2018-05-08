from tinydb import TinyDB
import os
from flask import Flask
import Timetable
import datetime

timetable_db = TinyDB('timetable_db.json')
app = Flask(__name__)

# Gets environment variables
school = str(os.environ["school"])
user = str(os.environ["user"])
password = str(os.environ["password"])

@app.route("/")
def run_flask():
    today = datetime.datetime.now().strftime("%A")
    try:
        tt = Timetable.read_db(timetable_db)
        return Timetable.get_day(tt, today, 1).return_html()
    except TypeError:
        tt = Timetable.get_timetable(school, user, password)
        Timetable.write_db(tt, timetable_db)
        return Timetable.get_day(tt, today, 1).return_html()
