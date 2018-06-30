import requests
import os

class TestApp(object):
        def test_client_updating(self):
                username = str(os.environ["username"])
                password = str(os.environ["password"])
                headers = {"username": username, "password": password, "update":"True"}
                url = "http://127.0.0.1:5000/list"
                r = requests.post(url=url, headers=headers)
                json = r.json()
                assert json[0]["session1"]["Info"]["Class"] != None
        def test_client(self):
                username = str(os.environ["username"])
                headers = {"username": username}
                url = "http://127.0.0.1:5000/list"
                r = requests.get(url=url, headers=headers)
                json = r.json()
                assert json[0]["session1"]["Info"]["Class"] != None