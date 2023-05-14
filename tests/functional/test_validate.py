from tests.functions import *
import pytest
import time


def test_validate(client):
    master_path = "./app/data/"

    graph = [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}]
    modules = [{"name": "MYSQLInput", "type": "Input", "code": "class Module():..."}, {"name": "MYSQLOutput", "type": "Output", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "MYSQLOutput2", "type": "Output", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "MYSQLOutput4", "type": "Output", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "Postgres", "type": "input", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "Julio", "type": "input", "module": "a"}, {"name": "dummyTransform", "type": "Transform", "code": "def process_item(message):\n    print(message)\n    return message", "description": "Dummy module", "type_in": ["str"], "type_out": ["str"]}]

    modify_file(f"{master_path}graph.json", graph, "JSON")
    modify_file(f"{master_path}modules.json", modules, "JSON")

    response = client.get('/system/restart')
    assert response.status_code == 200

    res = client.get('/system/status')
    while res.json["response"][0]["status"] == "RESTARTING":
        time.sleep(1)
        res = client.get('/system/status')