import os
import re
import mechanicalsoup
from tinydb import TinyDB, where
import json

tinydb = TinyDB('./db.json')
school = str(os.environ["school"])


class main():
        def update(self, user, password):
                try:
                        print("update starting")
                        br = mechanicalsoup.StatefulBrowser(user_agent='Timetable scraping Bot: https://github.com/ire4ever1190/app4flask')
                        url = "http://{}.app4.ws/".format(school)

                        br.open(url)
                        br.select_form(nr=0)
                        br["txtLoginUserID"] = user
                        br["txtLoginPassword"] = password
                        br.submit_selected()
                        br.open(url + str("portal/timetable.php"))

                        classes = br.get_current_page().find_all('td', {"width": '18%'})
                        # timetable_list, room_list, teacher_list, time_list = []
                        room_list = []
                        teacher_list = []
                        time_list = []
                        timetable_list = []
                        # find the tag holding the classes and get the text
                        for i in classes:
                                classes = i.find_all('span', {"class": "ttsub"})
                                extrainfo = i.find_all('span', {"class": "ttname"})

                                for ii in classes:
                                        timetable_list.append(ii.text.strip())
                                for iii in extrainfo:
                                        # Find things such has teacher names, times and rooms using regex
                                        try:
                                                search = str(iii)
                                                room = re.search(r'([A-Z])\w+\d', search)
                                                room_list.append(room.group())

                                                teacher = re.search(r'([A-Z]+[a-z])\w+\s+\w+\w', search)
                                                teacher_list.append(teacher.group())

                                                time = re.search(r'([0-9])+:+\w+', search)
                                                time_list.append(time.group())
                                        # This is just for lunch since lunch doesn't have extra info
                                        except:
                                                room_list.append("Outside")
                                                teacher_list.append(" ")
                                                time_list.append(" ")

                        # use start and end to break the the main into into smaller lists of days
                        def daylist(start, end):

                                daytimetable_list = []
                                dayroom_list = []
                                dayteacher_list = []
                                daytime_list = []

                                for i in range(start, end):
                                        daytimetable_list.append(timetable_list[i])
                                        dayroom_list.append(room_list[i])
                                        dayteacher_list.append(teacher_list[i])
                                        daytime_list.append(time_list[i])
                                return daytimetable_list, dayroom_list, dayteacher_list, daytime_list

                        # insert data into database
                        def inset(start, end, dayid, user):

                                session = 1
                                classes, rooms, teachers, times = daylist(start, end)

                                for clas, room, teacher, time in (zip(classes, rooms, teachers, times)):

                                        clas = str(clas)
                                        room = str(room)
                                        teacher = str(teacher)
                                        time = str(time)

                                        tinydb.insert({'Day': dayid, 'Session': session, 'User': user, 'Info':{
                                                'Class': clas,
                                                 'Time': time,
                                                 'Room': room,
                                                 'Teacher': teacher}
                                                })

                                        session += 1

                        dayid = 1
                        start = 0
                        end = 9
                        # add classes to database

                        while dayid <= 10:

                                inset(start, end, dayid, user)
                                dayid += 1
                                start += 9
                                end += 9

                        print("database updated")

                except TypeError:
                        print("connection unreliable, please try again later")
                        pass

        # This turns
        def getjson(self, day, session, user):

                jsonstr = tinydb.get((where('Day') == day) & (where('Session') == session) & (where('User') == user))
                print(jsonstr)
                return jsonstr

        def get(self, day, session, user, item):
                jsonstr = tinydb.get((where('Day') == day) & (where('Session') == session) & (where('User') == user))
                parse = jsonstr["Info"][item]
                return parse
