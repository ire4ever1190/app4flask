# app4flask
[![pipeline status](https://gitlab.com/ire4ever1190/app4flask/badges/master/pipeline.svg)](https://gitlab.com/ire4ever1190/app4flask/commits/master)
=======
## This is now hosted on gitlab [here](https://gitlab.com/ire4ever1190/app4flask)
#### THIS DOES NOT WORK ON ITS OWN
#### YOU MUST HAVE AN APP4 ACCOUNT
#### FOR THIS TO WORK
This is a simple flask server to scrape your timetable from app4 website then display it has a simple to parse webpage so that it can be 
displayed in things such has an web app or in things such has conky/rainmeter

To run first clone this then cd into the dir then run.
```
sudo pip install -r requirements.txt
```
Then set your schools name from the command line.
You find the school name by looking at the app4 url
https://{ This is your school name}.app4.ws
```
export school={{ school name }}
```

Then to run the server first cd into 'app4flask' then run.
```
python app.py
```
your timetable will be served at 127.0.0.1:5000/(user name)/(password)/list
on first time run give it a minute or two so that it can scrape your timetable and add it to the database.

If you want to host it, you need to set up a uWSGI/nginx config or use gunicorn.

###Using the api
###---

once you have successfully installed the flask app and are hosting it somewhere
you probably want to start using it. If you want to just view it like a website
then just navigate to the index page. If you want to use this in your own 
script or program then it's very easy to get the info. Here is an example
to get the current days timetable then to get the first sessions class.
```
>>> import requests
>>> headers = {"username": username}
>>> # Or if you want to update the database has well
>>> headers = {"username": username, "password": password, "update":"True"}
>>> url = "http://yoururl/list"
>>> r = requests.post(url=url, headers=headers)
>>> json = r.json()
>>> print(json[0]["session1"]["info"]["class"])

```

Current options
---

##### /list 
It returns timetable, 
classroom, teacher and time.
(only meant to be accessed from script)

##### /list/(day)
Displays a basic list but for a certain day.
(only meant to be accessed from script)

##### /
Displays a form to enter username and password which then displays
your timetable in a human readable format.

### Development

To use the tests you need to run 
```
sudo pip install -r devrequirements.txt
```
Then to run tests you run
```
cd app4flask
tox
```
