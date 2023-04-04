from flask import jsonify
from app.helpers.controller import controller
import zmq
import json
import os


def update(request, name):
    data = request.get_json()

    singleton = controller()

    try:
        if os.path.getsize('./app/data/modules.json') == 0:
            raise Exception("File Empty")

        with open('./app/data/modules.json', 'w+') as module_file:
            modules = json.load(module_file)

            index = None
            for i, mod in enumerate(modules):
                if mod['name'] == name:
                    index = i
                    if name + '.py' in os.listdir('./app/data/modules'):
                        os.remove('./app/data/modules/' + name + '.py')
                        with open('./app/data/modules/' + data['name'] + '.py', 'w') as file:
                            file.write(data['code'])
                    else:
                        raise Exception("Module does not exist")
                    break

            if index is not None:
                modules[index] = data
            else:
                raise Exception("Module does not exist")
            

            with open('./app/data/modules.json', 'w') as module_file:
                json.dump(modules, module_file) 

        for message in singleton.send_message("RESTART"):
            if message != "200":
                raise Exception("")
            
        return jsonify({"status": 200})
    except Exception as e:
        return jsonify(
            {"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400}
        )
