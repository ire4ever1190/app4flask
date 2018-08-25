import os

import mechanicalsoup
from tinydb import TinyDB, where

tinydb = TinyDB('./db.json')
school = str(os.environ["school"])


class main():
        def update(self, user, password):
                try:
                        print("update starting")
                        url = "https://{}.app4.ws/".format(school)

                        br = mechanicalsoup.StatefulBrowser(user_agent='Timetable scraping Bot: https://gitlab.com/ire4ever1190/app4flask')
                        br.set_verbose(2)
                        br.open(url)
                        br.select_form(nr=0)
                        br["txtLoginUserID"] = user
                        br["txtLoginPassword"] = password
                        br.submit_selected()
                        br.open(url + str("portal/timetable.php"))
                        classes = br.get_current_page().find_all('td', {'class': ['ttblue', 'ttgreen']})

                        room_list = []
                        teacher_list = []
                        time_list = []
                        timetable_list = []
                        # find the tag holding the classes and get the text
                        for classeshtml in classes:
                                classes = classeshtml.find_all('span', {"class": "ttsub"})
                                extrainfo = classeshtml.find_all('span', {"class": "ttname"})

                                for i in classes:
                                        timetable_list.append(i.text.strip())
                                for i in extrainfo:
                                        # Find things such has teacher names, times and rooms using self.find_between
                                        presearch = self.find_between(str(i), '<br/>', '<br/>')
                                        room = self.find_between(str(i), presearch + '<br/>', '</span>')
                                        room_list.append(room)

                                        teacher = self.find_between(str(i), '<span class="ttname">', '<br/>')
                                        teacher_list.append(teacher)

                                        teacher_list.append("No one listed")

                                        # Time has a space at the start so it is removed
                                        time = str(self.find_between(str(i), '<br/>', '<br/>')).replace(" ","")
                                        time_list.append(time)
                                        # This is just for lunch since lunch doesn't have extra info

                        # use start and end to break the the main into into smaller lists of days
                        def day_list(start, end):

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
                                classes, rooms, teachers, times = day_list(start, end)

                                for clas, room, teacher, time in (zip(classes, rooms, teachers, times)):

                                        clas = str(clas)
                                        room = str(room)
                                        teacher = str(teacher)
                                        time = str(time)

                                        # Upsert means that if its there it will update it
                                        # but if its not then it will create it
                                        tinydb.upsert({'Day': dayid, 'Session': session, 'User': user, 'Info': {
                                                'Class': clas,
                                                 'Time': time,
                                                 'Room': room,
                                                 'Teacher': teacher}
                                                }, (where('Day') == dayid) &
                                                   (where('Session') == session) &
                                                   (where('User') == str(user)))

                                        session += 1

                        start = 0
                        end = 9
                        # add classes to database

                        for dayid in range(0, 10):

                                inset(start, end, dayid, user)
                                start += 9
                                end += 9

                        print("database updated")

                except TypeError:
                        print("connection unreliable, please try again later")
                        pass

        # This returns pure json from database
        def get_json(self, day, session, user):
                return tinydb.get((where('Day') == day) & (where('Session') == session) & (where('User') == str(user)))

        # This returns structured specific data from database
        def get(self, day, session, user, item):
                jsonstr = tinydb.get((where('Day') == day) & (where('Session') == session) & (where('User') == str(user)))
                parse = jsonstr["Info"][item]
                return parse

        def find_between(self, s, first, last ):
                start = s.index(first) + len(first)
                end = s.index(last, start)
                return s[start:end]