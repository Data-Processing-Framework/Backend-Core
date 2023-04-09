from flask import jsonify
import json
import os


def get(request, name):

    # All modules
    try:
        if len(name) == 0:
            if "modules.json" not in os.listdir("./app/data/"):
                raise Exception("File does not exist")

            if os.path.getsize("./app/data/modules.json") == 0:
                raise Exception("File Empty")

            with open("./app/data/modules.json", "r") as module_file:
                modules = json.load(module_file)
                return modules

        # Just one module
        else:

            if "modules.json" not in os.listdir("./app/data/"):
                raise Exception("File does not exist")

            if os.path.getsize("./app/data/modules.json") == 0:
                raise Exception("File Empty")

            with open("./app/data/modules.json", "r") as module_file:
                modules = json.load(module_file)
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
