from flask import jsonify
import zmq


def update(request, moduleId):
    print("HERE")
    data = request.get_json()

    name = data['name']
    type = data['type']
    module = data['module']

    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    try:
        socket.connect("ipc://backend.ipc")

        try:
            socket.send_string(f'{name};{type};{module};PUT;MODULE;{moduleId}')

            try:
                message = socket.recv()

                if message == '200':
                    return jsonify({"status": 200})
                else:
                    return jsonify({"errors": [{"error": "", "message": "", "detail": ""}], "code": 400})
                
            except Exception as e:
                return jsonify({"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400})
            
        except Exception as e:
            return jsonify({"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400})
        
    except Exception as e:
        return jsonify({"errors": [{"error": "", "message": str(e), "detail": ""}], "code": 400})
