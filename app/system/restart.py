from flask import jsonify
from app.helpers.controller import controller

def restart(request):
    Controll = controller()
    try:
        Answer = Controll.send_message("RESTART")
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
                                "error": "Restart fail",
                                "message": str(e),
                                "detail": "stop the computer and open the computer again"
                            }
                        ],
                        "code": 400
                    }
                ),
                400,
            )
