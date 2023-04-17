from flask import jsonify
from app.helpers.controller import controller


def status():  # funcion inventada, luego sera status.py
    status = 200
    return status


def start(request):

    try:
        controlador = controller()
        missatge = str("START")
        resposta = controlador.send_message(missatge)

        if resposta["code"] == 200:
            print("start")
            return jsonify({"status": 200})
        else:
            return resposta, 400

    except Exception as e:
        if str(e) == "Server is already on.":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Server already on",
                                "message": str(e),
                                "detail": "Server is already on, START only works when server ain't already running",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
        elif str(e) == "Server couldn't be started.":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Server couldn't start",
                                "message": str(e),
                                "detail": "Server couldn't get started",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
