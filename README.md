## app4flask
This flask application uses mechanicalsoup to scrape app4 for your timetable than hosts a website with today's current timetable.

To run first clone this then cd into the dir then run
```
pip install -r requirements.txt
```
Then export your school identifyer, your username and password.
e.g,
```
export school=highschool
export user=12345
export password=password
```
Next you will need to export index.py to FLASK_APP
```
export FLASK_APP=index.py flask run
```
Finally, simply run flask.
```
python3 -m flask run
```
Or in python2.
```
python -m flask run
```
Your timetable will be served at localhost:5000/
