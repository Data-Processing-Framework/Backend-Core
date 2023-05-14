from tests.functions import *
import pytest
import time
import threading

class RequestThread(threading.Thread):
    def __init__(self, url, data, client):
        threading.Thread.__init__(self)
        self.url = url
        self.data = data
        self.response = None
        self.client = client
    
    def run(self):
        self.response = self.client.post(self.url, json=self.data)

        while True:
            status_res = self.client.get('/system/status')
            while "response" not in list(status_res.json.keys()):
                status_res = self.client.get('/system/status')
                time.sleep(1)
            status = status_res.json["response"][0]["status"]
            if status != "RESTARTING":
                break
        time.sleep(1)


@pytest.mark.parametrize("json",  [
    ({
        "data": [
            {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
            {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
        ],
        "file_names": [
            "prova.py",
            "prova2.py"
        ],
        "responses": {
            "thread1": [200, True],
            "thread2": [200, True]
        }
    }),
    ({
        "data": [
            {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
            {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
        ],
        "file_names": [
            "prova.py",
            "prova2.py"
        ],
        "responses": {
            "thread1": [400, True, "Module with the same name already exists"],
            "thread2": [400, True, "Module with the same name already exists"]
        }
    }),
    ({
        "data": [
            {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
            {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
        ],
        "file_names": [
            "prova.py",
            "prova2.py"
        ],
        "responses": {
            "thread1": [400, True, "The field 'description' is missing from the JSON"],
            "thread2": [400, True, "The field 'description' is missing from the JSON"]
        }
    })
])
def test_module_post_locks(client, json):
    urls = ["/module/", "/module/"]

    thread1 = RequestThread(urls[0], json["data"][0], client)
    thread2 = RequestThread(urls[1], json["data"][1], client)

    time.sleep(5)
    
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print(thread1.response.status_code)
    print(thread2.response.status_code)
    print(file_exists(json["file_names"][0], "./app/data/modules/"))
    print(file_exists(json["file_names"][1], "./app/data/modules/"))

    assert thread1.response.status_code == json["responses"]["thread1"][0]
    assert thread2.response.status_code == json["responses"]["thread2"][0]

    assert file_exists(json["file_names"][0], "./app/data/modules/") == json["responses"]["thread1"][1]
    assert file_exists(json["file_names"][1], "./app/data/modules/") == json["responses"]["thread2"][1]

    if json["responses"]["thread1"] > 2:
         assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread1"][2]

    if json["responses"]["thread2"] > 2:
         assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread2"][2]

    time.sleep(5)