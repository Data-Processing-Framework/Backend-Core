import os

from flask import jsonify

from app.helpers.controller import controller
from app.helpers.file_locker import block_write



def update(request):
    try:
        data = request.get_json()
        singleton = controller()
        
        if os.path.getsize("./app/data/graph.json") == 0:
            raise Exception("File Empty")
        
        block_write("./app/data/graph.json", data)

        message = singleton.send_message("RESTART")

        if message["code"] == 200:
            return jsonify(message), 200
        else:
            return jsonify(message), 400

    except Exception as e:
        if str(e) == "File Empty":
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
