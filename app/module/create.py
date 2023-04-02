import json
from flask import jsonify
from app.helpers import controller

import zmq


def create(request):

    request_json = request.get_json()
    singleton = controller()
    try:
        for message in singleton.send_message(f"CREATE;MODULE;{json.dumps(request_json)}"):
            if message != "200":
                raise Exception("")
        return jsonify({"status": 200})
    except Exception as e:
        return jsonify(
            {"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400}
        )
