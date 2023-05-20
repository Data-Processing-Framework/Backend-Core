# from tests.functions import *
# import pytest
# import time
# import threading

# class RequestThread(threading.Thread):
#     def __init__(self, url, data, client, option):
#         threading.Thread.__init__(self)
#         self.url = url
#         self.data = data
#         self.response = None
#         self.client = client
#         self.option = option
    
#     def run(self):
#         if self.option == "POST":
#             self.response = self.client.post(self.url, data=self.data, content_type="multipart/form-data")
#         elif self.option == "DELETE":
#             self.response = self.client.delete(self.url, json=self.data)
#         elif self.option == "PUT":
#             self.response = self.client.put(self.url, data=self.data, content_type="multipart/form-data")
#         elif self.option == "GET":
#             self.response = self.client.get(self.url)

#         while True:
#             status_res = self.client.get('/system/status')
#             while "response" not in list(status_res.json.keys()):
#                 status_res = self.client.get('/system/status')
#                 time.sleep(1)
#             status = status_res.json["response"][str(list(status_res.json["response"].keys())[0])]["status"]
#             if status != "RESTARTING":
#                 break
#         time.sleep(15)


# @pytest.mark.parametrize("json",  [
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [200, True],
#             "thread2": [200, True]
#         },
#         "tag": "POST"
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, True, "Module with the same name already exists"],
#             "thread2": [400, True, "Module with the same name already exists"]
#         },
#         "tag": "POST"
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, True, "The field 'description' is missing from the JSON"],
#             "thread2": [400, True, "The field 'description' is missing from the JSON"]
#         },
#         "tag": "POST"
#     })
# ])
# def test_module_post_locks(client, json):
#     time.sleep(15)
#     urls = ["/module", "/module"]

#     file1 = open(f"./tests/data/{json['file_names'][0]}", "rb")
#     json["data"][0]["code"] = (file1, json['file_names'][0])
#     file2 = open(f"./tests/data/{json['file_names'][1]}", "rb")
#     json["data"][1]["code"] = (file2, json['file_names'][1])

#     thread1 = RequestThread(urls[0], json["data"][0], client, json["tag"])
#     thread2 = RequestThread(urls[1], json["data"][1], client, json["tag"])

#     time.sleep(5)
    
#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

#     assert thread1.response.status_code == json["responses"]["thread1"][0]
#     assert thread2.response.status_code == json["responses"]["thread2"][0]

#     assert file_exists(json["file_names"][0], "./app/data/modules/") == json["responses"]["thread1"][1]
#     assert file_exists(json["file_names"][1], "./app/data/modules/") == json["responses"]["thread2"][1]

#     if len(json["responses"]["thread1"]) > 2:
#         assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread1"][2]

#     if len(json["responses"]["thread2"]) > 2:
#         assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread2"][2]

#     time.sleep(5)


# @pytest.mark.parametrize("json",  [
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [200, False],
#             "thread2": [200, False]
#         }
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, False, "Module does not exist"],
#             "thread2": [400, False, "Module does not exist"]
#         }
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, False, "File Empty"],
#             "thread2": [400, False, "File Empty"]
#         },
#         "extra": {}
#     })
# ])
# def test_module_delete_locks(client, json):
#     time.sleep(15)
#     if "extra" in list(json.keys()):
#         remove_size("modules.json")
    
#     time.sleep(5)

#     urls = ["/module/", "/module/"]

#     thread1 = RequestThread(urls[0] + json["file_names"][0].split(".")[0], json["data"][0], client, "DELETE")
#     thread2 = RequestThread(urls[1] + json["file_names"][1].split(".")[0], json["data"][1], client, "DELETE")

#     time.sleep(5)
    
#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

#     assert thread1.response.status_code == json["responses"]["thread1"][0]
#     assert thread2.response.status_code == json["responses"]["thread2"][0]

#     assert file_exists(json["file_names"][0], "./app/data/modules/") == json["responses"]["thread1"][1]
#     assert file_exists(json["file_names"][1], "./app/data/modules/") == json["responses"]["thread2"][1]

#     if len(json["responses"]["thread1"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread1"][2]

#     if len(json["responses"]["thread2"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread2"][2]

#     if "extra" in list(json.keys()):
#         return_size("modules.json")
    
#     res = client.get('/system/status')
#     while res.json["response"][str(list(res.json["response"].keys())[0])]["status"] == "RESTARTING":
#         time.sleep(1)
#         res = client.get('/system/status')
    
#     time.sleep(5)


# @pytest.mark.parametrize("json",  [
#     ({
#         "data": [
#             {"name": "Julio", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "Postgres", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "Julio.py",
#             "Postgres.py"
#         ],
#         "responses": {
#             "thread1": [200, True],
#             "thread2": [200, True]
#         }
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, False, "Module does not exist"],
#             "thread2": [400, False, "Module does not exist"]
#         }
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, False, "File Empty"],
#             "thread2": [400, False, "File Empty"]
#         },
#         "extra": {}
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, False, "The field 'description' is missing from the JSON"],
#             "thread2": [400, False, "The field 'description' is missing from the JSON"]
#         }
#     })
# ])
# def test_module_put_locks(client, json):
#     time.sleep(15)
#     if "extra" in list(json.keys()):
#         remove_size("modules.json")
    
#     time.sleep(5)

#     urls = ["/module/", "/module/"]

#     file1 = open(f"./tests/data/{json['file_names'][0]}", "rb")
#     json["data"][0]["code"] = (file1, json['file_names'][0])
#     file2 = open(f"./tests/data/{json['file_names'][1]}", "rb")
#     json["data"][1]["code"] = (file2, json['file_names'][1])

#     thread1 = RequestThread(urls[0] + json["file_names"][0].split(".")[0], json["data"][0], client, "PUT")
#     thread2 = RequestThread(urls[1] + json["file_names"][1].split(".")[0], json["data"][1], client, "PUT")

#     time.sleep(5)
    
#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

#     assert thread1.response.status_code == json["responses"]["thread1"][0]
#     assert thread2.response.status_code == json["responses"]["thread2"][0]

#     assert file_exists(json["file_names"][0], "./app/data/modules/") == json["responses"]["thread1"][1]
#     assert file_exists(json["file_names"][1], "./app/data/modules/") == json["responses"]["thread2"][1]

#     if len(json["responses"]["thread1"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread1"][2]

#     if len(json["responses"]["thread2"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread2"][2]

#     if "extra" in list(json.keys()):
#         return_size("modules.json")
    
#     res = client.get('/system/status')
#     while res.json["response"][str(list(res.json["response"].keys())[0])]["status"] == "RESTARTING":
#         time.sleep(1)
#         res = client.get('/system/status')
    
#     time.sleep(5)


# @pytest.mark.parametrize("json",  [
#     ({
#         "data": [
#             {"name": "Julio", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "Postgres", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "Julio.py",
#             "Postgres.py"
#         ],
#         "responses": {
#             "thread1": [200, True],
#             "thread2": [200, True]
#         }
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, False, "Module does not exist"],
#             "thread2": [400, False, "Module does not exist"]
#         }
#     }),
#     ({
#         "data": [
#             {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
#             {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"}
#         ],
#         "file_names": [
#             "prova.py",
#             "prova2.py"
#         ],
#         "responses": {
#             "thread1": [400, False, "File Empty"],
#             "thread2": [400, False, "File Empty"]
#         },
#         "extra": {}
#     })
# ])
# def test_module_get_locks(client, json):
#     time.sleep(15)
#     if "extra" in list(json.keys()):
#         remove_size("modules.json")
    
#     time.sleep(5)

#     urls = ["/module/", "/module/"]

#     thread1 = RequestThread(urls[0] + json["file_names"][0].split(".")[0], json["data"][0], client, "GET")
#     thread2 = RequestThread(urls[1] + json["file_names"][1].split(".")[0], json["data"][1], client, "GET")

#     time.sleep(5)
    
#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

#     assert thread1.response.status_code == json["responses"]["thread1"][0]
#     assert thread2.response.status_code == json["responses"]["thread2"][0]

#     assert file_exists(json["file_names"][0], "./app/data/modules/") == json["responses"]["thread1"][1]
#     assert file_exists(json["file_names"][1], "./app/data/modules/") == json["responses"]["thread2"][1]

#     if len(json["responses"]["thread1"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread1"][2]

#     if len(json["responses"]["thread2"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread2"][2]

#     if "extra" in list(json.keys()):
#         return_size("modules.json")
    
#     res = client.get('/system/status')
#     while res.json["response"][str(list(res.json["response"].keys())[0])]["status"] == "RESTARTING":
#         time.sleep(1)
#         res = client.get('/system/status')
    
#     time.sleep(5)


# @pytest.mark.parametrize("json",  [
#     ({
#         "data": [
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}],
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}]
#         ],
#         "responses": {
#             "thread1": [200],
#             "thread2": [200]
#         }
#     }),
#     ({
#         "data": [
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}],
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}]
#         ],
#         "responses": {
#             "thread1": [400, "File Empty"],
#             "thread2": [400, "File Empty"]
#         },
#         "extra": {}
#     })
# ])
# def test_graph_get_locks(client, json):
#     time.sleep(15)
#     if "extra" in list(json.keys()):
#         remove_size("graph.json")
    
#     time.sleep(5)

#     urls = ["/graph/", "/graph/"]

#     thread1 = RequestThread(urls[0], json["data"][0], client, "GET")
#     thread2 = RequestThread(urls[1], json["data"][1], client, "GET")

#     time.sleep(5)
    
#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

#     assert thread1.response.status_code == json["responses"]["thread1"][0]
#     assert thread2.response.status_code == json["responses"]["thread2"][0]

#     if len(json["responses"]["thread1"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread1"][2]

#     if len(json["responses"]["thread2"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread2"][2]

#     if "extra" in list(json.keys()):
#         return_size("graph.json")
    
#     res = client.get('/system/status')
#     while res.json["response"][str(list(res.json["response"].keys())[0])]["status"] == "RESTARTING":
#         time.sleep(1)
#         res = client.get('/system/status')
    
#     time.sleep(5)


# @pytest.mark.parametrize("json",  [
#     ({
#         "data": [
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}],
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}]
#         ],
#         "responses": {
#             "thread1": [200],
#             "thread2": [200]
#         }
#     }),
#     ({
#         "data": [
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}],
#             [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}]
#         ],
#         "responses": {
#             "thread1": [400, "File Empty"],
#             "thread2": [400, "File Empty"]
#         },
#         "extra": {}
#     }),
#     ({
#         "data": [
#             [{"name": "Input1", "type": "Input", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}],
#             [{"name": "Input1", "type": "Input", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}]
#         ],
#         "responses": {
#             "thread1": [400, "The field 'module' is missing from the JSON"],
#             "thread2": [400, "The field 'module' is missing from the JSON"]
#         }
#     })
# ])
# def test_graph_put_locks(client, json):
#     time.sleep(15)
#     if "extra" in list(json.keys()):
#         remove_size("graph.json")
    
#     time.sleep(5)

#     urls = ["/graph/", "/graph/"]

#     thread1 = RequestThread(urls[0], json["data"][0], client, "PUT")
#     thread2 = RequestThread(urls[1], json["data"][1], client, "PUT")

#     time.sleep(5)
    
#     thread1.start()
#     thread2.start()

#     thread1.join()
#     thread2.join()

#     assert thread1.response.status_code == json["responses"]["thread1"][0]
#     assert thread2.response.status_code == json["responses"]["thread2"][0]

#     if len(json["responses"]["thread1"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread1"][2]

#     if len(json["responses"]["thread2"]) > 2:
#          assert thread1.response.json["errors"][0]["message"] == json["responses"]["thread2"][2]

#     if "extra" in list(json.keys()):
#         return_size("graph.json")
    
#     res = client.get('/system/status')
#     while res.json["response"][str(list(res.json["response"].keys())[0])]["status"] == "RESTARTING":
#         time.sleep(1)
#         res = client.get('/system/status')
    
#     time.sleep(5)