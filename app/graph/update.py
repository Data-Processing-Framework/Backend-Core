from flask import jsonify
import json
import os


def update(request):
    data = request.get_json()

    try:
        if "graph.json" not in os.listdir("./app/data/"):
            raise Exception("File does not exist")
        
        if os.path.getsize("./app/data/graph.json") == 0:
            raise Exception("File Empty")
        
        with open("./app/data/graph.json", "w") as graph_file:
            json.dump(data, graph_file)

        return jsonify("OK"), 200

    except Exception as e:
        if str(e) == "File does not exist":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Core error",
                                "message": str(e),
                                "detail": "Please check the file name and location and try again.",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
        elif str(e) == "File Empty":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Core error",
                                "message": str(e),
                                "detail": "Please create a module before updating it, and then try again.",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
        else:
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Core error",
                                "message": str(e),
                                "detail": "Please try again.",
                            }
                        ],
                        "code": 400,
                    }
                ),
                400,
            )
