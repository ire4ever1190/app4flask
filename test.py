import app
import os
import datetime

username = str(os.environ["username"])
password = str(os.environ["password"])
def test_updater():
        assert app.data.update(username, password) != '0'


def test_info():
        today = datetime.datetime.today().weekday()
        classes = []
        for i in range(1, 10):
                classes.append("<class>" + str(app.data.get(today, i, username, "class")) + "</class>")
                timetablefordaylist = ''.join(classes)
        assert app.show_info(username, password) == timetablefordaylist


def test_extrainfo():
        today = datetime.datetime.today().weekday()
        classes = []
        items = ["class", "time", "teacher", "room"]
        for i in range(1, 10):
                for x in items:
                        # Formats the info into tags e.g. <teacher> #Teacher name# </teacher>
                        info = "<{}>{}</{}>".format(x, app.data.get(today, i, username, x), x)
                        classes.append(info)
        timetablefordaylist = ''.join(classes)
        assert app.show_extrainfo(username, password) == timetablefordaylist

