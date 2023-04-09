from flask import jsonify
from app.helpers.controller import controller
import json
import os


def get(request, name):

    if len(name) == 0:
        general_modules = True
    else:
        general_modules = False
    # All modules
    if general_modules:
        if "modules.json" not in os.listdir("./app/data/"):
            raise Exception("File does not exist")

        if os.path.getsize("./app/data/modules.json") == 0:
            raise Exception("File Empty")

        with open("./app/data/modules.json", "r") as module_file:
            modules = json.load(module_file)
            return modules

    # Just one module
    else:

        try:

            if "modules.json" not in os.listdir("./app/data/"):
                raise Exception("File does not exist")

            if os.path.getsize("./app/data/modules.json") == 0:
                raise Exception("File Empty")

            with open("./app/data/modules.json", "r") as module_file:
                modules = json.load(module_file)
            
            modules = modules["modules"]
            for mod in modules:
                if mod["name"] == name:
                    return mod
        except Exception as e:
            if str(e) == "File does not exist":
                return (
                    jsonify(
                        {
                            "errors": [
                                {
                                    "error": "Core error",
                                    "message": str(e),
                                    "detail": "Please check the file name and location and try again.",
                                }
                            ],
                            "code": 400,
                        }
                    ),
                    400,
                )
            elif str(e) == "File Empty":
                return (
                    jsonify(
                        {
                            "errors": [
                                {
                                    "error": "Core error",
                                    "message": str(e),
                                    "detail": "Please create a module before updating it, and then try again.",
                                }
                            ],
                            "code": 400,
                        }
                    ),
                    400,
                )
            elif str(e) == "Module does not exist":
                return (
                    jsonify(
                        {
                            "errors": [
                                {
                                    "error": "Core error",
                                    "message": str(e),
                                    "detail": "Please check the module name and try again.",
                                }
                            ],
                            "code": 400,
                        }
                    ),
                    400,
                )
            else:
                return (
                    jsonify(
                        {
                            "errors": [
                                {
                                    "error": "Core error",
                                    "message": str(e),
                                    "detail": "Please try again.",
                                }
                            ],
                            "code": 400,
                        }
                    ),
                    400,
                )
