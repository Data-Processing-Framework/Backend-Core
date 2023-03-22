from flask import jsonify


def get(request, moduleId):
    return jsonify({"status": 200})  # Exemple de resposta
