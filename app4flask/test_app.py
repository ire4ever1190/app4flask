import requests
import os
import mechanicalsoup
from tinydb import TinyDB


tinydb = TinyDB('./db.json')
def browser_base_login():
        s = requests.Session()
        br = mechanicalsoup.StatefulBrowser(session=s)
        br.open("http://127.0.0.1:5000/login")
        br.select_form(nr=0)
        username = str(os.environ["username"])
        password = str(os.environ["password"])
        br["username"] = username
        br["password"] = password
        return br

class TestApp(object):
        def test_client_updating(self):
                username = str(os.environ["username"])
                password = str(os.environ["password"])
                headers = {"student_num": username, "password": password, "update":"True"}
                url = "http://127.0.0.1:5000/list"
                r = requests.post(url=url, headers=headers)
                json = r.json()
                assert json[0]["session1"]["Info"]["Class"] != None


        def test_client_updating_get(self):
                username = str(os.environ["username"])
                password = str(os.environ["password"])
                headers = {"student_num": username, "password": password, "update":"True"}
                url = "http://127.0.0.1:5000/list"
                r = requests.get(url=url, headers=headers)
                text = r.text
                assert text == "Please make a POST request when updating and not a GET request"


        def test_browser_normal(self):
                br = browser_base_login()
                br.submit_selected()
                assert br.get_current_page().find('title').text.strip() is not "Title"

        def test_browser_remember_me_cookies(self):
                br = browser_base_login()
                br["remember"] = "y"
                br.submit_selected()
                assert br.session.cookies.get_dict()['student_num'] == str(os.environ["username"])

        def test_browser_remember_me_login(self):
                br = browser_base_login()
                br["remember"] = "y"
                br.submit_selected()
                br.open("http://127.0.0.1:5000/login")
                assert br.get_current_page().find('title').text.strip() is not "Title"



