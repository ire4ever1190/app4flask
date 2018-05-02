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
Finally, simply run the script which start flask automatically.
```
python3 index.py
```
Or in python2.
```
python2 index.py
```
Your timetable will be served at [localhost:5000](http://localhost:5000/)
