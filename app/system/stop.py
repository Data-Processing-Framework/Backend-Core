from flask import jsonify
from app.helpers.controller import controller

def status():  # To be deleted
    status = 200
    return status


def stop(request):
    try:
        controlador = controller()
        resposta = controlador.send_message("STOP")

        if resposta["code"] == 200:
            return jsonify({"status": 200})
        else:
            return resposta, 400

    except Exception as e:
        return (
            jsonify(
                {
                    "errors": [
                        {
                            "error": "Stop failed",
                            "message": str(e),
                            "detail": "Try again and check if it is already stoped.",
                        }
                    ],
                    "code": 400,
                }
            ),
            400,
        )
        
