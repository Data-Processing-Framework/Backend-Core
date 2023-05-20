from app.helpers.file_locker import *
from tests.functions import *
import pytest
import time
import os


def test_validate(client):
    master_path = "./app/data/"

    if "prova.py" in os.listdir(f"{master_path}modules/"):
        block_delete(f"{master_path}modules/prova.py")

    if "prova2.py" in os.listdir(f"{master_path}modules/"):
        block_delete(f"{master_path}modules/prova2.py")

    graph = [{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}]
    modules = [{"name": "MYSQLInput", "type": "Input", "code": "class Module():..."}, {"name": "MYSQLOutput", "type": "Output", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "MYSQLOutput2", "type": "Output", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "MYSQLOutput4", "type": "Output", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "Postgres", "type": "input", "code": "class Module():\n    def __init__(self):\n       pass"}, {"name": "Julio", "type": "input", "module": "a"}, {"name": "dummyTransform", "type": "Transform", "code": "def process_item(message):\n    print(message)\n    return message", "description": "Dummy module", "type_in": ["str"], "type_out": ["str"]}]

    block_write(f"{master_path}graph.json", graph)
    block_write(f"{master_path}modules.json", modules)

    # while True:
    #     status_res = client.get('/system/status')
    #     while "response" not in list(status_res.json.keys()):
    #         status_res = client.get('/system/status')
    #         time.sleep(1)
    #     status = status_res.json["response"][0]["status"]
    #     if status != "RESTARTING":
    #         break
    #     time.sleep(1)