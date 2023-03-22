from flask import jsonify


def create(request):
    return jsonify({"status": 200, "errors": ["bad parsing"]})  # Exemple de resposta
