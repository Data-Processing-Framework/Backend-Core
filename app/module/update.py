from flask import jsonify
from helpers.controller import controller
import zmq


def update(request, name):
    data = request.get_json()

    type = data["type"]
    module = data["module"]

    singleton = controller()

    try:
        for message in singleton.send_message(f"PUT;MODULE;{name};{type};{module}"):
            if message != "200":
                raise Exception("")
            
        return jsonify({"status": 200})
    except Exception as e:
        return jsonify(
            {"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400}
        )
