import mechanicalsoup
import re
from Day import Day
from Session import Session

def get_timetable(school, user, password):
    # App4 Timetable Url with school identifier
    url = "http://{}.app4.ws/portal/timetable.php".format(school)
    # Creates a browser. Then opens the Timetable Url which leads to a login page
    br = mechanicalsoup.StatefulBrowser()
    br.open(url)
    # Log in using user and password
    br.select_form(nr=0)
    br["txtLoginUserID"] = user
    br["txtLoginPassword"] = password
    br.submit_selected()
    # With Permission reopens the Timetable page
    br.open(url)
    # Makes a soup of the pages html
    page = br.get_current_page()
    # Gets everyday's html
    daysRaw = page.find_all('td', {"width": '18%'})
    # Empty Container to be populated with day objects
    timetable = []
    for day in daysRaw:
        # Variables with Day args
        day_name = day.find_all("td", {"class": re.compile("^ttdark")})[0].string.extract()
        day_id = daysRaw.index(day)+1
        # Appends a Day Object and Passes an empty list to be populated bt Session Objects, day_name and day_id
        timetable.append(Day([], day_name, day_id))
        # List with all day's sessions html
        sessions = day.find_all("td", {"class": re.compile("^tt")})
        # Iterates through all sessions appending a Session object to each Day object
        for session in sessions:
            # If session is a session continue
            if len(session.find_all("td")) > 0:
                # Variables with Session args
                session_number = int(session.find_all("td")[0].string.extract())
                session_code = session.find_all("td")[1].find_all("span")[0].string.extract()
                # List of teacher, room and time
                session_periph = session.find_all("td")[1].find_all("span")[1].get_text("|").split("|")
                # Appends a Session Object to current day (i.e, days[-1])
                # Checks if it is not an empty session (e.g, Lunch, Community Service)
                if len(session_periph) > 2:
                    timetable[-1].append(
                        Session(
                            session_number,
                            session_code,
                            session_periph[0],
                            str(session_periph[1]).strip(),
                            session_periph[2]
                        )
                    )
                # If it is an empty session do not pass a teacher or room
                else:
                    timetable[-1].append(
                        Session(
                            session_number,
                            session_code,
                            session_periph[0],
                            None,
                            None
                        )
                    )
    return timetable
def write_db(timetable, db):
    # Clears database so it can be written over
    db.purge()
    # Appends a Day object passsing day_name, day_id and sessions
    for day in timetable:
        sessions = []
        for session in day:
            sessions.append(
                {
                    'number': session.number,
                    'code': session.code,
                    'teacher': session.teacher,
                    'room': session.room,
                    'time': session.time
            }
            )
        db.insert({
            'day_name': day.day_name,
            'day_id': day.day_id,
            'sessions': sessions
        })
        {
            'number': session.number,
            'code': session.code,
            'teacher': session.teacher,
            'room': session.room,
            'time': session.time
        }
def read_db(db):
    # Clears timetable so it can be overwritten
    timetable = []
    # Loops over timetable every day and
    for day in db.all():
        # Creates a local empty lsit to be populated with database session
        sessions = []
        # Appends a Session to current day passing session number, code, teacher, room, time
        for session in day['sessions']:
            sessions.append(Session(
                session['number'],
                session['code'],
                session['teacher'],
                session['room'],
                session['time']
            ))
        # Appends a Day object passing session, day_name, day_id
        timetable.append(
            Day(
                sessions,
                day['day_name'],
                day['day_id']
            )
        )
    return timetable
def get_day(tt, day_name, week):
    days = list(filter(lambda day: day.day_name == day_name, tt))
    try:
        return days[0] if days[0].week_id == week else days[1]
    except IndexError:
        return Day([], day_name, 0)
