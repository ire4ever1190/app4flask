import requests
import os
import mechanicalsoup

class TestApp(object):
        def test_client_updating(self):
                username = str(os.environ["username"])
                password = str(os.environ["password"])
                headers = {"student_num": username, "password": password, "update":"True"}
                url = "http://127.0.0.1:5000/list"
                r = requests.post(url=url, headers=headers)
                json = r.json()
                assert json[0]["session1"]["Info"]["Class"] != None

        def test_browser(self):
                br = mechanicalsoup.StatefulBrowser()
                br.open("http://127.0.0.1:5000/login")
                br.select_form(nr=0)
                username = str(os.environ["username"])
                password = str(os.environ["password"])
                br["username"] = username
                br["password"] = password
                br.submit_selected()
                assert br.get_current_page().find('title').text.strip() is not "Title"
