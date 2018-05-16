from flask import Flask, render_template, Markup, request
import datetime
import datahandler
import Forms
from flask import jsonify
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
                classes = []
                # Makes a json list of all the classes of the day
                for i in range(1, 10):
                                classes.append(data.getjson(today,i,username))
                print(classes)
                return jsonify(classes)
        # if there not in the database this except gets raised and updates the timetable
        except datahandler.mechanicalsoup.LinkNotFoundError:
                data.update(username, password)
                return show_info(username, password)

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
        except datahandler.mechanicalsoup.LinkNotFoundError:
                data.update(username, password)
                return show_info(username, password)


# This doesn't need a route. It is only used by the index route
def show_webapp(studentnum, password):
        try:
                # Gets the day of the week has a int e.g. Monday = 0, Tuesday = 1
                today = datetime.datetime.today().weekday()
                today += 1
                classes = []
                items = ["class", "time", "teacher", "room"]
                for session in range(1, 10):
                        for x in items:
                                # Formats the info into tags e.g. <teacher> #Teacher name# </teacher>
                                info = "<{}>{}</{}>".format(x, data.get(today, session, studentnum, x), x)
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
        # If they clicked update timetable this is called
        if form.update.data == True:
                data.update(form.username.data, form.password.data)
        # When they press submit then there shown there timetable
        if form.validate_on_submit():
                return show_webapp(form.username.data, form.password.data)
        return render_template('Login.html', form=form)


@app.route('/sw.js')
def showsw():
        return app.send_static_file('sw.js')

if __name__ == '__main__':
        app.run()



#TODO fix week2 issue??? it's kind of working
