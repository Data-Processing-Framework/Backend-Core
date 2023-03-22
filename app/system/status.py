from flask import jsonify


def status(request):
    return jsonify({"status": 200})  # Exemple de resposta
