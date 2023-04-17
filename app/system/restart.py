from flask import jsonify
from app.helpers.controller import controller

def restart(request):
    Controll = controller()
    try:
        Answer = Controll.send_message("RESTART")
        return jsonify(Answer)  # Exemple de resposta
    except Exception as e:
        return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Type of error",
                                "message": "Error message",
                                "detail": "Restart fail"
                            }
                        ],
                        "code": 400
                    }
                ),
                400,
            )
