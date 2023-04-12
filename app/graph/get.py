from flask import jsonify
import json
import os


def get(request):
    try:
        if "graph.json" not in os.listdir("./app/data/"):
            raise Exception("File does not exist")
        else:
            with open("./app/data/graph.json", "r") as graph_file:
                graph = json.load(graph_file)
                return jsonify(graph), 200
    except Exception as e:
        return jsonify({"errors": [{"error": "Core error", "message": str(e), "detail": "PGraph does not exist, try adding a node"}], "code": 400}), 400
    
