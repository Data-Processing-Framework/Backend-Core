import os

from flask import jsonify

from app.helpers.controller import controller
from app.helpers.file_locker import block_read, block_write, block_delete


def update(request, name):
    try:
        data = request.get_json()
        singleton = controller()

        if os.path.getsize("./app/data/modules.json") == 0:
            raise Exception("File Empty")

        modules = block_read("./app/data/modules.json")

        index = None
        for i, mod in enumerate(modules):
            if mod["name"] == name:
                index = i
                if name + ".py" in os.listdir("./app/data/modules"):
                    block_delete("./app/data/modules/" + name + ".py")
                    block_write("./app/data/modules/" + data["name"] + ".py", data["code"])
                else:
                    raise Exception("Module does not exist")
                break
        if index is not None:
            modules[index] = data
        else:
            raise Exception("Module does not exist")

        block_write("./app/data/modules.json", modules)

        message = singleton.send_message("RESTART")

        if message["code"] == 200:
            return jsonify(message), 200
        else:
            return jsonify(message), 400

    except Exception as e:
        if str(e) == "File Empty":
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
        elif str(e) == "Module does not exist":
            return (
                jsonify(
                    {
                        "errors": [
                            {
                                "error": "Core error",
                                "message": str(e),
                                "detail": "Please check the module name and try again.",
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
