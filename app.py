from flask import Flask, render_template, Markup, Response
import datetime
import datahandler
app = Flask(__name__)
data = datahandler.main()
@app.route('/<studentnum>/<password>/list')
def show_info(studentnum, password):
        try:
                # Gets the day of the week has a int e.g. Monday = 0, Tuesday = 1
                today = datetime.datetime.today().weekday()
                classes = []
                for i in range(1, 10):
                        classes.append("<class>" + str(data.get(today, i, studentnum, "class")) + "</class>")
                        timetablefordaylist = ''.join(classes)
                return timetablefordaylist
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(studentnum, password)
                return "Please reload page"


@app.route('/<studentnum>/<password>/extralist')
def show_extrainfo(studentnum, password):
        try:
                # Gets the day of the week has a int e.g. Monday = 0, Tuesday = 1
                today = datetime.datetime.today().weekday()
                classes = []
                items = ["class", "time", "teacher", "room"]
                for i in range(1, 10):
                        for x in items:
                        # Formats the info into tags e.g. <teacher> #Teacher name# </teacher>
                                info = "<{}>{}</{}>".format(x, data.get(today, i, studentnum, x), x)
                                classes.append(info)
                timetablefordaylist = ''.join(classes)
                return timetablefordaylist
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(studentnum, password)
                return "Please reload page"

@app.route('/<studentnum>/<password>/list/<int:day>')
def show_info_certain_day(studentnum, password, day):
        try:
                # Day of the week is declared in the url week 1 is 1-5 and week 2 is 6-10
                classes = []
                for i in range(1, 10):
                        classes.append("<class>" + str(data.get(day, i, studentnum, "class")) + "</class>")
                        timetablefordaylist = ''.join(classes)
                return timetablefordaylist
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(studentnum, password)
                classes = []
                for i in range(1, 10):
                        classes.append("<class>" + str(data.get(day, i, studentnum, "class")) + "</class>")
                        timetablefordaylist = ''.join(classes)
                return timetablefordaylist

@app.route('/<studentnum>/<password>/webapp')
def show_webapp(studentnum, password):
        try:
                # Gets the day of the week has a int e.g. Monday = 0, Tuesday = 1
                today = datetime.datetime.today().weekday()
                classes = []
                items = ["class", "time", "teacher", "room"]
                for i in range(1, 10):
                        for x in items:
                        # Formats the info into tags e.g. <teacher> #Teacher name# </teacher>
                                info = "<{}>{}</{}>".format(x, data.get(today, i, studentnum, x), x)
                                classes.append(info)
                timetablefordaylist = ''.join(classes)
                timetablehtml = Markup(timetablefordaylist)
                # Return the template with variables
                return render_template('default.html',
                                        user=studentnum,
                                        content=timetablehtml,
                                        day=today)
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(studentnum, password)
                return "Please reload page"



# This is the index page usage is not yet implemented \_(-_-)_/.
@app.route('/')
def index():
        # So here the idea I will have a form here that you enter you username and password which redirects you
        # to the webapp. I will probably change the extra info to return json instead so it can be parsed super
        # easy
        return '\_(-_-)_/'


if __name__ == '__main__':
        app.run()



#TODO fix week2 issue

