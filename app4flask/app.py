import datetime
import pytz

from flask import Flask, render_template, Markup, request, make_response, jsonify

import Forms
import datahandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
data = datahandler.main()


# This returns a json list of the current day or if the day is passed in the url then it returns that
@app.route('/list/<today>', methods=['POST'])
@app.route('/list/', methods=['POST'])
@app.route('/list', methods=['POST'])
def show_info(today=None):
        print(request.headers.get('timezone'))
        if today is None:
                if request.headers.get('timezone') is None:
                        today = datetime.datetime.now(pytz.utc).weekday()
                else:
                        today = datetime.datetime.now(pytz.timezone(request.headers.get('timezone'))).weekday()
        today = int(today)
        username = str(request.headers.get('username'))
        if request.headers.get('update') == 'True':
                password = str(request.headers.get('password'))
                data.update(username, password)

        try:

                classes = [{'day': today}]

                # Gets json from database and creates the JSON that will be returned
                for i in range(1, 10):
                                classes[0]["session" + str(i)] = data.getjson(today, i, 37161)
                return jsonify(classes)
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(username)
                return show_info()


# This doesn't need a route. It is only used by the index route
def show_html(student_num):
                        return render_template('default.html',
                                        user=student_num,
                                        )


@app.route('/login')
@app.route('/')
def index():
        # This is the index page. It shows a form asking for username and password and if the person wants to update
        # there timetable / Remember them
        print(request.cookies.get('student_num'))
        print(request.method)
        if request.method == "POST":
                form = Forms.LoginForm(request.form)
                if form.update.data is True:
                        form = Forms.LoginForm(request.form)
                        data.update(form.username.data, form.password.data)
                        return show_html(form.username.data)

                # If they clicked remember me then cookies are made that last 6 months I think
                if form.remember.data is True:
                        response = make_response(show_html(form.username.data))
                        response.set_cookie('student_num', form.username.data, max_age=60 * 60 * 24 * 92)
                        return response

                return show_html(form.username.data)
        elif request.method == "GET":
                if request.cookies.get('student_num') != None:
                        return show_html(request.cookies.get('student_num'))




@app.route('/icons.ico')
def giveicon():
        return app.send_static_file('icons.ico')


@app.route('/sw.js')
def givesw():
        return app.send_static_file('sw.js')


if __name__ == '__main__':
        app.run()


# TODO fix week2 issue??? it's kind of working but I'm working on finding out how app4 checks the week
