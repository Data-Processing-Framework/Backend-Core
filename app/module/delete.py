from flask import jsonify
from app.helpers.controller import controller
import json
import os
import zmq


def delete(request, name):
    
    data = request.get_json()
    name = data["name"]
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    if "modules.json" not in os.listdir("./app/data/"):
            raise Exception("File does not exist")

    if os.path.getsize("./app/data/modules.json") == 0:
        raise Exception("File Empty")

    with open("./app/data/modules.json", "r") as module_file:
        modules = json.load(module_file)
    modules = modules["modules"]

    for module in modules:
        if module["name"] == name:
             module.pop(module)
        

    print(module)
    with open('./app/data/modules.json', 'w') as module_file:
        module_file.write('')
        module_file.close()
    with open("./app/data/modules.json", "r") as module_file:
        json.dump(module_file)
