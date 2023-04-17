from flask import jsonify

class status:
    def status(request):
        return jsonify({"status": 200})  # Exemple de resposta
