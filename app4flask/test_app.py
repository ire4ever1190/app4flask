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

def check_for_none(string):
        for i in range(0, 9):
                if string[0]["session" + str(i + 1)]["Info"]["Teacher"] is "None":
                        return False
                elif string[0]["session" + str(i + 1)]["Info"]["Time"] is "None":
                        return False
                elif string[0]["session" + str(i + 1)]["Info"]["Room"] is "None":
                        return False
                elif string[0]["session" + str(i + 1)]["Info"]["Class"] is "None":
                        return False
                else:
                        return True


class TestApp(object):
        def test_client_updating(self):
                username = str(os.environ["username"])
                password = str(os.environ["password"])
                headers = {"student_num": username, "password": password, "update": "True"}
                url = "http://127.0.0.1:5000/list"
                r = requests.post(url=url, headers=headers)
                print(r.text)
                json = r.json()
                assert json[0]["session1"]["Info"]["Class"] != None


        def test_client_updating_get(self):
                username = str(os.environ["username"])
                password = str(os.environ["password"])
                headers = {"student_num": username, "password": password, "update": "True"}
                url = "http://127.0.0.1:5000/list"
                r = requests.get(url=url, headers=headers)
                text = r.text
                assert text == "Please make a POST request when updating and not a GET request"


        def test_browser_normal(self):
                br = browser_base_login()
                br.submit_selected()
                assert br.get_current_page().find('title').text.strip() is not "Login"

        def test_browser_remember_me_cookies_check(self):
                br = browser_base_login()
                br["remember"] = "y"
                br.submit_selected()
                assert br.session.cookies.get_dict()['student_num'] == str(os.environ["username"])

        def test_browser_remember_me_cookies_login(self):
                br = browser_base_login()
                br["remember"] = "y"
                br.submit_selected()
                br.open("http://127.0.0.1:5000/login")
                assert br.get_current_page().find('title').text.strip() is not "Login"

        def test_browser_update(self):
                tinydb.purge()
                br = browser_base_login()
                br["update"] = "y"
                br.submit_selected()
                username = str(os.environ["username"])
                headers = {"student_num": username}
                url = "http://127.0.0.1:5000/list"
                response = requests.get(url, headers=headers)
                assert check_for_none(response.json()) is True

        def test_browser_update_cookies(self):
                tinydb.purge()
                br = browser_base_login()
                br["update"] = "y"
                br["remember"] = "y"
                br.submit_selected()
                username = str(os.environ["username"])
                headers = {"student_num": username}
                url = "http://127.0.0.1:5000/list"
                response = requests.get(url, headers=headers)
                assert check_for_none(response.json()) is True
                assert br.session.cookies.get_dict()['student_num'] == str(os.environ["username"])



