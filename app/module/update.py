from flask import jsonify
import zmq


def update(request, moduleId):
    data = request.get_json()

    name = data["name"]
    type = data["type"]
    module = data["module"]

    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    try:
        socket.connect("ipc://backend.ipc")
        socket.send_string(f"{name};{type};{module};PUT;MODULE;{moduleId}")
        message = socket.recv()

        if message == "200":
            return jsonify({"status": 200})
        else:
            raise Exception("")

    except Exception as e:
        return jsonify(
            {"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400}
        )
