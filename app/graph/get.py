from flask import jsonify
import json
import os
from app.helpers.file_locker import block_read


def get(request):
    try:
        if os.path.getsize("./app/data/graph.json") != 0:
            graph = block_read("./app/data/graph.json")
            return jsonify(graph), 200
        else:
            raise Exception("File Empty")
    except Exception as e:
        return (
            jsonify(
                {
                    "errors": [
                        {
                            "error": "Core error",
                            "message": str(e),
                            "detail": "Graph does not have nodes, try adding a node",
                        }
                    ],
                    "code": 400,
                }
            ),
            400,
        )
