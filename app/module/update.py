import os

from flask import jsonify

from app.helpers.controller import controller
from app.helpers.file_locker import block_read, block_write, block_delete, block_write_file


required_fields = ["name", "type", "description", "type_in", "type_out"]


class MissingFieldException(Exception):
    pass


def validate_json(json_data):

    for field in required_fields:
        if field not in json_data:
            raise MissingFieldException(f"The field '{field}' is missing from the JSON")


def update(request, name):
    try:
        # data = request.get_json()
        data["name"] = request.form.get("name")
        data["type"] = request.form.get("type")
        data["description"] = request.form.get("description")
        data["type_in"] = request.form.get("type_in")
        data["type_out"] = request.form.get("type_out")
        code = request.files.get("code")
        singleton = controller()

        validate_json(data)

        if os.path.getsize("./app/data/modules.json") == 0:
            raise Exception("File Empty")

        modules = block_read("./app/data/modules.json")

        if code:
            raw_code = block_read_python_file(f"./app/data/modules/{request_json['name']}.py")
            data["code"] = raw_code

        index = None
        for i, mod in enumerate(modules):
            if mod["name"] == name:
                index = i
                if name + ".py" in os.listdir("./app/data/modules"):
                    block_delete("./app/data/modules/" + name + ".py")
                    block_write_file("./app/data/modules/" + data["name"] + ".py", data["code"])
                else:
                    raise Exception("Module does not exist")
                break
        if index is not None:
            modules[index] = data
        else:
            raise Exception("Module does not exist")

        block_write("./app/data/modules.json", modules)

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