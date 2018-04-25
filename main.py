from tinydb import TinyDB, Query, where
from flask import Flask
import datetime
import requests
from bs4 import BeautifulSoup
import mechanize
app = Flask(__name__)

tinydb = TinyDB('db.json')
query = Query()

def update(userid, password):
        try:
                print("update starting")
                def browse():
                        #open a the login url then the timetable url after login
                        br = mechanize.Browser()
                        loginurl = "http://{{ school name }}.app4.ws/"
                        url = "http://{{ school name }}.app4.ws/portal/timetable.php"
                        br.open(loginurl)
                        print(br.title())
                        br.select_form(nr=0)
                        br["txtLoginUserID"] = userid
                        br["txtLoginPassword"] = password
                        br.submit()
                        print(br.title())
                        br.open(url)
                        soup = BeautifulSoup(br.response().read(), "lxml")
                        classes = soup.find_all('td', {"width": '18%'})
                        timetablelist = []
                        #find the tag holding th classes and get the text
                        for i in classes:
                                classes = i.find_all('span', {"class": "ttsub"})
                                for i in classes:
                                        timetablelist.append(i.text.strip())
                        return timetablelist
                timetablelist = browse()
                # use x and y to break the the main into into smaller lists of days

                def classlist(start, end, list):
                        classlist = []
                        for i in range(start ,end):
                                classlist.append(list[i])
                        return classlist
                # insert data into database

                def inset(start, end, iday, list, user):
                        session = 1
                        print(start, end)
                        classes = classlist(start, end, list)
                        for i in classes:
                                tinydb.insert({'Day': iday, 'Session': session, 'class': i, "user": user})
                                session += 1
                iday = 1
                start = 0
                end = 9
                # add classes to database
                while iday <= 10:
                        inset(start, end, iday, timetablelist, userid)
                        iday += 1
                        start += 9
                        end += 9

                print("database updated")

        except requests.exceptions.ConnectionError:
                print("connection unreliable")
                pass
# This the the certain session from the timetable

def get(day, session, user):
        jsonstr = tinydb.get((where('Day') == day) & (where('Session') == session) & (where('user') == user))
        print jsonstr
        parse = jsonstr["class"]
        return parse

@app.route('/<studentnum>/<password>/list')
def show_post(studentnum, password):
        try:
                today = datetime.datetime.today().weekday()
                classes = []

                for i in range(1, 10):
                        classes.append("<item>" + str(get(today, i, studentnum)) + "</item>")
                classeslist = ''.join(classes)
                return classeslist
        # If there not in the database this will add them
        except TypeError:
                update(studentnum, password)
                return "please stand by"


app.run()
