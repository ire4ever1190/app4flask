import datetime
import pytz

from flask import Flask
from flask import render_template, request, make_response, jsonify

import Forms
import datahandler
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
data = datahandler.main()


# This returns a json list of the current day
# or if the day is passed in the url then it returns that
@app.route('/list/<today>', methods=['POST'])
@app.route('/list/', methods=['POST'])
@app.route('/list', methods=['POST'])
def show_info(today=None):
        if today is None:
                if request.headers.get('timezone') is None:
                        today = datetime.datetime.now(pytz.utc).weekday()
                else:
                        timezone = pytz.timezone(request.headers.get('timezone'))
                        today = datetime.datetime.now(timezone).weekday()
        today = int(today)
        today += 1
        student_num = str(request.headers.get('student_num'))
        if request.headers.get('update') == 'True':
                password = str(request.headers.get('password'))
                data.update(student_num, password)

        try:

                classes = [{'day': today + 1}]

                # Gets json from database and creates the JSON that will be returned
                for i in range(1, 10):
                        classes[0]["session" + str(i)] = data.get_json(today, i, 37161)
                return jsonify(classes)
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                data.update(student_num, str(request.headers.get('password')))
                return show_html(student_num)


# This doesn't need a route. It is only used by the index route
def show_html(student_num):
        return render_template('default.html',
                               user=student_num,
                               )


@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
        # This is the index page. It shows a form asking for student_num and password
        # and if the person wants to update there timetable / Remember them
        form = Forms.LoginForm(request.form)
        if form.validate_on_submit():
                def update_data(student_num, password):
                        data.update(student_num, password)
                        return show_html(student_num)

                def remember_data(student_num):
                        response = make_response(show_html(student_num))
                        response.set_cookie('student_num', student_num, max_age=60 * 60 * 24 * 92)
                        return response

                # This make checks to see what buttons where clicked
                if form.update.data is True and form.remember.data is False:
                        return update_data(form.username.data, form.password.data)

                elif form.update.data is False and form.remember.data is True:
                        return remember_data(form.username.data)

                elif form.remember.data is True and form.update.data is True:
                        update_data(form.username.data, form.password.data)
                        return remember_data(form.remember.data)

                else:
                        return show_html(form.username.data)
        else:
                if request.cookies.get('student_num') is not None:
                        student_num = request.cookies.get('student_num')
                        return show_html(student_num)
                else:
                        form = Forms.LoginForm()
                        return render_template('Login.html',
                                               form=form
                                               )


@app.route('/icons.ico')
def giveicon():
        return app.send_static_file('icons.ico')


@app.route('/sw.js')
def givesw():
        return app.send_static_file('sw.js')


if __name__ == '__main__':
        app.run()

# TODO fix week2 issue???
# it's kind of working but I'm working on finding out how app4 checks the week
