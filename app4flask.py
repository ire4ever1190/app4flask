import datetime

import mechanicalsoup
import requests
from flask import Flask
from tinydb import TinyDB, Query, where

app = Flask(__name__)

tinydb = TinyDB('db.json')
query = Query()


def update(user, password):
        try:
                print("update starting")
                def browse():
                        br = mechanicalsoup.StatefulBrowser()
                        url = "http://{{ school name }}.app4.ws/"
                        br.open(url)
                        print(br.get_url())
                        br.select_form(nr=0)
                        br["txtLoginUserID"] = user
                        br["txtLoginPassword"] = password
                        br.submit_selected()
                        print(br.get_url())
                        print(url + str("/portal/timetable.php"))
                        br.open(url + str("portal/timetable.php"))
                        print(br.get_current_page())
                        classes = br.get_current_page().find_all('td', {"width": '18%'})
                        print(classes)
                        timetablelist = []
                        # find the tag holding the classes and get the text
                        for i in classes:
                                classes = i.find_all('span', {"class": "ttsub"})
                                for ii in classes:
                                        timetablelist.append(ii.text.strip())
                        return timetablelist
                timetablelist = browse()
                # use start and end to break the the main into into smaller lists of days
                def daylist(start, end, list):
                        daylist = []
                        print(start)
                        print(end)
                        for i in range(start, end):
                                print(i)
                                daylist.append(list[i])
                        return daylist
                # insert data into database
                def inset(start, end, dayid, list, user):
                        session = 1
                        print(start, end)
                        classes = daylist(start, end, list)
                        for i in classes:
                                tinydb.insert({'Day': dayid, 'Session':session, 'class': i,"user": user})
                                session += 1
                dayid = 1
                start = 0
                end = 9
                # add classes to database

                while dayid <= 10:

                        inset(start, end, dayid, timetablelist, user)
                        dayid += 1
                        start += 9
                        end += 9

                print("database updated")

        except requests.exceptions.ConnectionError:
                print("connection unreliable")
                pass

def get(day, session, user):
        jsonstr = tinydb.get((where('Day') == day) & (where('Session') == session) & (where('user') == user))
        print(jsonstr)
        parse = jsonstr["class"]
        return parse

@app.route('/<studentnum>/<password>/list')
def show_post(studentnum, password):
        try:
                today = datetime.datetime.today().weekday()
                classes = []
                for i in range(1, 10):
                        classes.append("<item>" + str(get(today, i, studentnum)) + "</item>")
                        timetablefordaylist = ''.join(classes)


                return timetablefordaylist
        # if there not in the database this except gets raised and updates the timetable
        except TypeError:
                update(studentnum, password)
                return "please stand by"


app.run()
#TODO use mechanical soup so this is compaitable with python 3

