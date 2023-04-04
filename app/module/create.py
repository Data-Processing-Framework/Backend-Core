import json
import os
from flask import jsonify
from app.helpers import controller


def create(request):
    # Get the request json data and create a singleton instance of the controller
    request_json = request.get_json()
    singleton = controller()
    try:
        # Check if the modules.json file is empty
        if os.path.getsize("./app/data/modules.json") == 0:
            with open("./app/data/modules.json", "w") as f:
                json.dump([request_json], f)
        else:
            with open("./app/data/modules.json", "r") as f:
                modules = json.load(f)

            # Check if the module already exists in the modules.json file
            for m in modules:
                if m["name"] == request_json["name"]:
                    raise Exception("Module with the same name already exists")

            # Add the module to the modules.json file and create a new file for the code of the module.
            modules.append(request_json)
            with open("./app/data/modules.json", "w") as f:
                json.dump(modules, f)
        # Create a new file for the code of the module.
        # If the python file for some unknown reason already exists, it will be overwritten.
        with open("./app/data/modules/" + request_json["name"] + ".py", "w") as f:
            f.write(request_json["code"])

        # Send a restart message to all the workers
        for message in singleton.send_message("RESTART"):
            if message != "200":
                raise Exception("")
        return jsonify({"status": 200})

    except Exception as e:
        return jsonify(
            {"errors": [{"error": "Biel no se que posar aqui", "message": str(e), "detail": "Crec que hi ha massa parametres per l'error"}], "code": 400}
        )
