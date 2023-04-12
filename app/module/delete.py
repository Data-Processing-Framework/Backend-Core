from flask import jsonify
from app.helpers.controller import controller
import json
import os


def delete(requests, name):
    
    singleton = controller()

    try:
        if "modules.json" not in os.listdir("./app/data/"):
                raise Exception("File does not exist")

        if os.path.getsize("./app/data/modules.json") == 0:
            raise Exception("File Empty")

        with open("./app/data/modules.json", "r") as module_file:
            modules = json.load(module_file)
            found = False

            for module in modules:
                if module["name"] == name:
                    modules.remove(module)
                    found = True
                    break

            if found:
                with open('./app/data/modules.json', 'w') as module_file:
                    json.dump(modules, module_file)

            if name + ".py" in os.listdir("./app/data/modules"):
                os.remove("./app/data/modules/" + name + ".py")
            else:
                raise Exception("Module does not exist")

        message = singleton.send_message("RESTART")

        if message["code"] == 200:
            return jsonify(message), 200
        else:
            return jsonify(message), 400
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

