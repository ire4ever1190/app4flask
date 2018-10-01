import datetime

import pytz
from flask import Flask
from flask import render_template, request, make_response, jsonify, redirect

import Forms
import datahandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
data = datahandler.main()


# This returns a json list of the current day
# or if the day is passed in the url then it returns that
@app.route('/list/<today>', methods=['POST', 'GET'])
@app.route('/list/', methods=['POST', 'GET'])
@app.route('/list', methods=['POST', 'GET'])
def show_info(today=None):
        # Checks if the day has been specified then if it hasn't it just goes with system timezone
        # If the timezone was specified then it reads the header and uses that
        if today is None:
                if request.headers.get('timezone') is None:
                        today = datetime.datetime.now().weekday()
                else:
                        timezone = pytz.timezone(request.headers.get('timezone'))
                        today = datetime.datetime.now(timezone).weekday()
        today = int(today)
        student_num = str(request.headers.get('student_num'))
        if request.headers.get('update') == 'True' and request.method == 'POST':
                password = str(request.headers.get('password'))
                data.update(student_num, password)
        elif request.headers.get('update') == 'True' and request.method == 'GET':
                return "Please make a POST request when updating and not a GET request"

        try:

                classes = [{'day': today}]

                # Gets json from database and creates the JSON that will be returned
                student_num = str(request.headers.get('student_num'))
                for i in range(1, 10):
                        classes[0]["session" + str(i)] = data.get_json(today, i, str(student_num))
                return jsonify(classes)
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                return "Please add add your info into the databasE"


# This doesn't need a route. It is only used by the index route
def show_html(student_num):
        return render_template('default.html', user=student_num, )


@app.route('/login')
@app.route('/', )
def index():
        # This is the index page. It shows a form asking for student_num and password
        # and if the person wants to update their timetable / Remember them
        form = Forms.LoginForm()
        return render_template('Login.html', form=form)


@app.route('/timetable', methods=['GET', 'POST'])
def timetable():
        def update_data(student_num, password):
                        data.update(student_num, password)
                        return show_html(student_num)

        def remember_data(student_num):
                        response = make_response(show_html(student_num))
                        response.set_cookie('student_num', student_num, max_age=60 * 60 * 24 * 92)
                        return response

        student_num = request.form.get('username')
        if request.form.get('password') is not None:
                password = request.form.get('password')
        remember_me = request.form.get('remember')
        update = request.form.get('update')
        if request.cookies.get('student_num') is not None:
                student_num = request.cookies.get('student_num')
                return show_html(student_num)

        elif request.cookies.get('student_num') is None and request.method == "GET":
                return redirect('/login')

        # This make checks to see what buttons where clicked

        if str(update) == 'y' and remember_me is None:
                return update_data(student_num, password)

        elif update is None and remember_me == 'y':
                return remember_data(student_num)

        elif update == 'y' and remember_me == 'y':
                update_data(student_num, password)
                return remember_data(student_num)

        else:
                return show_html(student_num)


@app.route('/sw.js')
def sw():
        return app.send_static_file('sw.js')


if __name__ == '__main__':
        app.run()

# TODO fix week2 issue???
# it's kind of working but I'm working on finding out how app4 checks the week
