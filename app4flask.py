import datetime
import re

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
                        br = mechanicalsoup.StatefulBrowser(user_agent='Timetable scraping Bot: https://github.com/ire4ever1190/app4flask')
                        url = "http://stpats.app4.ws/"

                        br.open(url)
                        print(br.get_url())
                        br.select_form(nr=0)
                        br["txtLoginUserID"] = user
                        br["txtLoginPassword"] = password
                        br.submit_selected()
                        print(br.get_url())
                        br.open(url + str("portal/timetable.php"))
                        classes = br.get_current_page().find_all('td', {"width": '18%'})
                        #timetable_list, room_list, teacher_list, time_list = []
                        room_list = []
                        teacher_list = []
                        time_list = []
                        timetable_list = []
                        # find the tag holding the classes and get the text
                        for i in classes:
                                classes = i.find_all('span', {"class": "ttsub"})
                                extrainfo = i.find_all('span', {"class": "ttname"})
                                for ii in classes:
                                        print(ii.text.strip())
                                        timetable_list.append(ii.text.strip())
                                for iii in extrainfo:
                                        # Find things such has teacher names, times and rooms
                                        try:
                                                search = str(iii)
                                                room = re.search(r'([A-Z])\w+\d', search)
                                                print(room.group())
                                                room_list.append(room.group())
                                                
                                                teacher = re.search(r'([A-Z]+[a-z])\w+\s+\w+\w', search)
                                                print(teacher.group())
                                                teacher_list.append(teacher.group())

                                                time = re.search(r'([0-9])+:+\w+', search)
                                                print(time.group())
                                                time_list.append(time.group())
                                        # This is just for lunch since lunch doesn't have extra info
                                        except:
                                                room_list.append("Outside")
                                                teacher_list.append(" ")
                                                time_list.append(" ")
                                                pass

                        return timetable_list, room_list, teacher_list, time_list

                timetable_list, room_list, teacher_list, time_list = browse()
                for i in timetable_list, room_list, teacher_list, time_list:
                        print(i)

                # use start and end to break the the main into into smaller lists of days
                def daylist(start, end, timetablelist, roomlist, teacherlist, timelist):
                        daytimetable_list = []
                        dayroom_list = []
                        dayteacher_list = []
                        daytime_list = []

                        for i in range(start, end):
                                daytimetable_list.append(timetablelist[i])
                                dayroom_list.append(roomlist[i])
                                dayteacher_list.append(teacherlist[i])
                                daytime_list.append(timelist[i])
                                print(timetablelist[i], roomlist[i], teacherlist[i], timelist[i])
                        return daytimetable_list, dayroom_list, dayteacher_list, daytime_list

                # insert data into database
                def inset(start, end, dayid, user, timetable_list, room_list, teacher_list, time_list):
                        session = 1
                        classes, rooms, teachers, times = daylist(start, end, timetable_list, room_list, teacher_list, time_list)

                        for clas, room, teacher, time in (zip(classes, rooms, teachers, times)):
                                clas = str(clas)
                                room = str(room)
                                teacher = str(teacher)
                                time = str(time)
                                tinydb.insert({'Day': dayid, 'Session': session, 'class': clas, "user": user, "time": time, "room": room, "teacher": teacher})
                                session += 1
                dayid = 1
                start = 0
                end = 9
                # add classes to database

                while dayid <= 10:
                        inset(start, end, dayid, user, timetable_list, room_list, teacher_list, time_list)
                        dayid += 1
                        start += 9
                        end += 9

                print("database updated")

        except requests.exceptions.ConnectionError:
                print("connection unreliable, please try again later")
                pass


def get(day, session, user):
        jsonstr = tinydb.get((where('Day') == day) & (where('Session') == session) & (where('user') == user))
        print(jsonstr)
        parse = jsonstr["class"]
        return parse


@app.route('/<studentnum>/<password>/list')
def show_post(studentnum, password):
        try:
                # Gets the day of the week has a int e.g. Monday = 0, Tuesday = 1
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


#app.run()
update(37161, "gold4green")
#TODO see if pypy can speed up the updating

