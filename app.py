from flask import Flask, render_template, Markup, request, redirect
import datetime
import datahandler
import Forms
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
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
                return show_info(studentnum, password)


@app.route('/<studentnum>/<password>/extralist', methods=['POST'])
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
                return show_extrainfo(studentnum, password)
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
                return show_info_certain_day(studentnum, password, day)


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
                return show_webapp()


@app.route('/', methods=['GET', 'POST'])
def index():
        # This is the index page. It shows a form asking for username and password and if the person wants to update
        # there timetable.
        form = Forms.LoginForm(request.form)
        # If they clicked update timetable this is runned
        if form.update.data == True:
                data.update(form.username.data, form.password.data)
        # When they press submit then there shown there timetable
        if form.validate_on_submit():
                return show_webapp(form.username.data, form.password.data)
        return render_template('Login.html', form=form)


@app.route('/<username>/<password>/sw.js')
def showsw(username, password):
        return app.send_static_file('sw.js')

if __name__ == '__main__':
        app.run()



#TODO fix week2 issue

