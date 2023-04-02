from flask import jsonify
from app.helpers.controller import controller
import zmq
import json


def update(request, name):
    data = request.get_json()

    singleton = controller()

    try:
        for message in singleton.send_message(f"PUT;MODULE;{json.dumps(data)}"):
            if message != "200":
                raise Exception("")
            
        return jsonify({"status": 200})
    except Exception as e:
        return jsonify(
            {"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400}
        )
