import datetime

from flask import Flask, render_template, Markup, request, make_response, json
from flask import jsonify

import Forms
import datahandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
data = datahandler.main()


# This returns a json list of the current day
@app.route('/list', methods=['POST'])
def show_info():
        username = str(request.headers.get('username'))
        if request.headers.get('update') == 'True':
                password = str(request.headers.get('password'))
                data.update(username, password)

        try:
                # Gets the day of the week has a int e.g. Monday = 0, Tuesday = 1
                today = datetime.datetime.today().weekday()
                classes = [{'day': today}]
                # Makes a json list of all the classes of the day

                for i in range(1, 10):
                                # classes.append(data.getjson(today, i, username))
                                classes[0]["session" + str(i)] = data.getjson(today, i, username)
                return jsonify(classes)
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(username)
                return show_info()


# This return a json list of a certain day e.g. /list/0 gives you the list of monday
@app.route('/list/<day>', methods=['POST'])
def show_info_certain_day(day):
        username = str(request.headers.get('username'))

        if request.headers.get('update') == 'True':
                password = str(request.headers.get('password'))
                data.update(username, password)

        try:
                classes = []
                # Makes a json list of all the days
                for session in range(1, 10):
                                classes.append(data.getjson(day, session, username))
                return jsonify(classes)
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(username, password)
                return show_info()


# This doesn't need a route. It is only used by the index route
def show_webapp(student_num, password=None):
        try:
                # Gets the day of the week has a int e.g. Monday = 0, Tuesday = 1
                today = datetime.datetime.today().weekday()
                today += 1
                classes = []
                items = ["Class", "Time", "Teacher", "Room"]


                for session in range(1, 10):
                        for x in items:
                                # Formats the info into tags e.g. <teacher> #Teacher name# </teacher>  data.get(today, session, student_num, x)
                                info = "<{}> Foo </{}>".format(x, x)
                                classes.append(info)

                timetablefordaylist = ''.join(classes)
                timetablehtml = Markup(timetablefordaylist)

                # Return the template with variables
                return render_template('default.html',
                                        user=student_num,
                                        content=timetablehtml,
                                        )
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(student_num, password)
                return show_webapp()


@app.route('/', methods=['GET', 'POST'])
def index():
        # This is the index page. It shows a form asking for username and password and if the person wants to update
        # there timetable / Remember them
        if not request.cookies.get('student_num'):
                form = Forms.LoginForm(request.form)
                # If they clicked update timetable this is called
                if form.update.data == True:
                        data.update(form.username.data, form.password.data)

                # If they clicked remember me then cookies are made
                if form.remember.data == True:
                        response = make_response(show_webapp(form.username.data, form.password.data))
                        response.set_cookie('student_num', form.username.data, max_age=60*60*24*92)
                        return response


                # When they press submit then there shown there timetable
                if form.validate_on_submit():
                        return show_webapp(form.username.data, form.password.data)

                return render_template('Login.html', form=form)
        else:
                return show_webapp(request.cookies.get('student_num'), "3003200337161")


@app.route('/icons.ico')
def giveicon():
        return app.send_static_file('icons.ico')


@app.route('/sw.js')
def givesw():
        return app.send_static_file('sw.js')


if __name__ == '__main__':
        app.run()


# TODO fix week2 issue??? it's kind of working
