from flask import jsonify
from helpers.controller import controller
import zmq


def create(request):

    request_json = request.get_json()
    name = request_json["name"]
    type = request_json["type"]
    module = request_json["module"]

    # Preparem la connexio amb el worker
    singleton = controller()
    try:
        for message in singleton.send_message(f"CREATE;MODULE;{name};{type};{module}"):
            if message != "200":
                raise Exception("")
        return jsonify({"name": name, "id": id, "type": type, "module": module}, 200)
    except Exception as e:
        return jsonify(
            {"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400}
        )
