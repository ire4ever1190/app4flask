import datetime
import os

from flask import Flask
from tinydb import TinyDB

import Timetable

timetable_db = TinyDB('timetable_db.json')
app = Flask(__name__)

# Gets environment variables
school = str(os.environ["school"])
user = str(os.environ["user"])
password = str(os.environ["password"])

@app.route("/<week>")
def run_flask(week):
    today = datetime.datetime.now().strftime("%A")
    try:
        tt = Timetable.read_db(timetable_db)
        return "<head><link rel='stylesheet' href='static/style.css'</link></head>" + Timetable.get_day(tt, today, int(week)).return_html()
    except TypeError:
        tt = Timetable.get_timetable(school, user, password)
        Timetable.write_db(tt, timetable_db)
        return "<head><link rel='stylesheet' href='static/style.css'</link></head>" + Timetable.get_day(tt, today, int(week)).return_html()
   
app.run()
