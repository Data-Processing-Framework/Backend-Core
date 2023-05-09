import os

from flask import jsonify

from app.helpers.controller import controller
from app.helpers.file_locker import block_write

required_fields = ["name", "type", "module", "inputs", "position"]


class MissingFieldException(Exception):
    pass


def validate_json(json_data):

    for field in required_fields:
        for node in json_data:
            if field not in node:
                raise MissingFieldException(
                    f"The field '{field}' is missing from the JSON"
                )


def update(request):
    try:
        data = request.get_json()
        singleton = controller()

        validate_json(data)

        if os.path.getsize("./app/data/graph.json") == 0:
            raise Exception("File Empty")

        block_write("./app/data/graph.json", data)

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