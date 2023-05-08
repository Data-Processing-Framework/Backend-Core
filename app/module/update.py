from flask import jsonify
from app.helpers.controller import controller
import json
import os

required_fields = ["name", "type", "description", "type_in", "type_out", "code"]


class MissingFieldException(Exception):
    pass


def validate_json(json_data):

    for field in required_fields:
        if field not in json_data or not json_data[field]:
            raise MissingFieldException(f"The field '{field}' is missing from the JSON")


def update(request, name):
    try:
        data = request.get_json()

        singleton = controller()

        validate_json(data)

        if "modules.json" not in os.listdir("./app/data/"):
            raise Exception("File does not exist")

        if os.path.getsize("./app/data/modules.json") == 0:
            raise Exception("File Empty")

        with open("./app/data/modules.json", "r") as module_file:
            modules = json.load(module_file)

            index = None
            for i, mod in enumerate(modules):
                if mod["name"] == name:
                    index = i
                    if name + ".py" in os.listdir("./app/data/modules"):
                        os.remove("./app/data/modules/" + name + ".py")
                        with open(
                            "./app/data/modules/" + data["name"] + ".py", "w"
                        ) as file:
                            file.write(data["code"])
                    else:
                        raise Exception("Module does not exist")
                    break

            if index is not None:
                modules[index] = data
            else:
                raise Exception("Module does not exist")

            with open("./app/data/modules.json", "w") as module_file:
                json.dump(modules, module_file)

        message = singleton.send_message("RESTART")

        if message["code"] == 200:
            return jsonify(message), 200
        else:
            return jsonify(message), 400

    except MissingFieldException as e:
        return (
            jsonify(
                {
                    "errors": [
                        {
                            "error": "User error",
                            "message": str(e),
                            "detail": "Fill the empty field",
                        }
                    ],
                    "code": 400,
                }
            ),
            400,
        )

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
