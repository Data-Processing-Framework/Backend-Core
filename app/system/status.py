from flask import jsonify
from app.helpers.controller import controller


def status(request):
    try:
        Controll = controller()
        Answer = Controll.send_message("STATUS")
        if Answer["code"] == 400:
            return jsonify(Answer), 400
        else:
            return jsonify(Answer), 200
    except Exception as e:
        return (
            jsonify(
                {
                    "errors": [
                        {
                            "error": "Error getting status of workers",
                            "message": str(e),
                            "detail": "Try to do this action later",
                        }
                    ],
                    "code": 400,
                }
            ),
            400,
        )