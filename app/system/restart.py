from flask import jsonify
from app.helpers.controller import controller

def restart(request):
    Answer = controller.send_message("restart")
    return jsonify(Answer)  # Exemple de resposta
