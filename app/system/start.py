from flask import jsonify
from app.helpers.controller import controller

def start(request):
    
    try:
        controlador = controller()
        resposta = controlador.send_message("START")

        if resposta["code"] == 200:
            return jsonify(resposta), 200
        else:
            return jsonify(resposta), 400
        
    except Exception as e:
        return (
            jsonify(
                {
                    "errors": [
                        {
                            "error": "Server already on",
                            "message": str(e),
                            "detail": "Server is already on, START only works when server ain't already running"
                        }
                    ],
                    "code": 400,
                }
            ),
            400,
        )
