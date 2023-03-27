from flask import jsonify
import zmq


def create(request):

    request_json = request.get_json()
    name = request_json["name"]
    id = request_json["id"]
    type = request_json["type"]
    module = request_json["module"]

    # Preparem la connexio amb el worker
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    try:
        # Ens connectem al worker
        socket.connect("ipc://backend.ipc")  # TODO: No sabem la adreça de connexio

        try:
            # Enviem el missatge
            socket.send_json({"name": name, "id": id, "type": type, "module": module})
            print("Sent request")
            try:
                # Esperem la resposta
                message = socket.recv()
                print("Received reply")
                if message == "200":
                    return jsonify({"status": 200})
                else:
                    # TODO: Especificar el error
                    return jsonify( 
                        {
                            "errors": [
                                {
                                    "error": "",
                                    "message": "Creation Failed",
                                    "detail": "Module already exists",
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
