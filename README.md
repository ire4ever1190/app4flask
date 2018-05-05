# app4flask


This is a simple flask server to scrape your timetable from app4 website then display it has a simple to parse webpage so that it can be 
displayed in things such has an app or in things such has conky/rainmeter

To run first clone this then cd into the dir then run
```
pip install -r requirements.txt
```
Then set your schools name from the command line
```
export school={{ school name }}
```

Then to run the server
```
python app4flask.py
```
your timetable will be served at 127.0.0.1:5000/(user name)/(password)/list
on first time run give it a minute or two so that it can scrape your timetable and add it to the database

If you want to host it, you need to set up a uWSGI config

Current options
---

##### /(user)/(password)/list
Display a basic list where it just displays the timetable


##### /(user)/(password)/extralist
Displays more info then the basic list, It displays timetable, 
classroom, teacher, time

##### /(user)/(password)/list/(day)
Displays a basic list but for a certain day
