from module_m import addToList, n_module, getList, createModule
from flask import jsonify
import zmq

#get the  module

def get(request, moduleId):
    
    print(request)
    request = str(request)
    id = request.split("/")[4]
    id = id.split("'")[0]
    print("The final id is: ", id)

    # Preparem la connexio amb el worker
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    try:
        # Ens connectem al worker
        socket.connect("ipc://backend.ipc")  # TODO: No sabem la adreça de connexio

        try:
            # Enviem el missatge
            socket.send_json({"id": id})
            try:
                # Esperem la resposta
                message = socket.recv()
                if message == "200":
                    return jsonify({"status": 200})
                else:
                    # TODO: Especificar el error
                    return jsonify( 
                        {
                            "errors": [
                                {
                                    "error": "",
                                    "message": "Get Failed",
                                    "detail": " ",
                                }
                            ],
                            "code": 400,
                        }
                    )
            except Exception as e:
                # TODO: Especificar el error
                return jsonify(
                    {
                        "errors": [
                            {"error": "", "message": str(e), "detail": "Receive Failed"}
                        ],
                        "code": 400,
                    }
                )
        except Exception as errorSending:
            # TODO: Especificar el error
            return jsonify(
                {
                    "errors": [
                        {"error": "", "message": str(errorSending), "detail": "Send Failed"}
                    ],
                    "code": 400,
                }
            )

    except Exception as errorConnecting:
        # TODO: Especificar el error
        return jsonify(
            {
                "errors": [
                    {"error": "", "message": str(errorConnecting), "detail": "Connection Failed"}
                ],
                "code": 400,
            }
        )
