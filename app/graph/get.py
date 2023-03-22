from flask import jsonify


def get(request):
    return jsonify({"status": 200})  # Exemple de resposta
