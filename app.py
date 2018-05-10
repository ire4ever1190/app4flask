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


# This is the login page usage is not yet implemented \_(-_-)_/.
@app.route('/', methods=['GET', 'POST'])
def index():
        # So here the idea I will have a form here that you enter you username and password which redirects you
        # to the webapp. I will probably change the extra info to return json instead so it can be parsed super
        # easy
        form = Forms.LoginForm(request.form)
        if form.update.data == True:
                data.update(form.username.data, form.password.data)

        if form.validate_on_submit():
                return redirect('/{}/{}/webapp'.format(form.username.data, form.password.data))
        return render_template('Login.html', form=form)


@app.route('/<username>/<password>/sw.js')
def showsw(username, password):
        return app.send_static_file('sw.js')

if __name__ == '__main__':
        app.run()



#TODO fix week2 issue

