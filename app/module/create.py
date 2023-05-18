import os

from flask import jsonify

from app.helpers.controller import controller
from app.helpers.file_locker import block_read, block_write

required_fields = ["name", "type", "description", "type_in", "type_out"]


class MissingFieldException(Exception):
    pass


def validate_json(json_data):

    for field in required_fields:
        if field not in json_data:
            raise MissingFieldException(f"The field '{field}' is missing from the JSON")


def create(request):

    try:
        request_json = {}
        # Get the request data and create a singleton instance of the controller
        request_json["name"] = request.form.get("name")
        request_json["type"] = request.form.get("type")
        request_json["description"] = request.form.get("description")
        request_json["type_in"] = request.form.get("type_in")
        request_json["type_out"] = request.form.get("type_out")
        code = request.files.get("code")
        singleton = controller()

        validate_json(request_json)
        # Check if the modules.json file is empty
        if os.path.getsize("./app/data/modules.json") == 0:
            print("Modules file is empty")
            block_write("./app/data/modules.json", [request_json])
        else:
            # Get all the modules from the modules.json file
            print("Modules file is not empty")
            modules = block_read("./app/data/modules.json")
            print(modules)
            # Check if the module already exists in the modules.json file
            for m in modules:
                if m["name"] == request_json["name"]:
                    raise Exception("Module with the same name already exists")
                
            # Create a new file (or overwrite) for the code of the module.
            if code:
                code.save(f"./app/data/modules/{request_json['name']}.py")
            else:
                raise Exception("No code file (.py) uploaded.")

            # Add the module to the modules.json file and create a new file for the code of the module.
            modules.append(request_json)
            block_write("./app/data/modules.json", modules)
        
        # Send a restart message to all the workers
        message = singleton.send_message("RESTART")
        if message["code"] == 200:
            return jsonify(message), 200
        else:
            return jsonify(message), 400

    # If an error occurs, return the corresponding error message
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
        if str(e) == "Workers could not be restarted":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Error Worker",
                                "message": str(e),
                                "detail": "Try restarting the system",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
        elif str(e) == "Module with the same name already exists":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Error Core",
                                "message": str(e),
                                "detail": "Try changing the name of the module",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
        elif str(e) == "No code file (.py) uploaded.":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Error Core",
                                "message": str(e),
                                "detail": "Try uploading file again",
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
                                "error": "Unknown Error",
                                "message": str(e),
                                "detail": "Try again later",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
