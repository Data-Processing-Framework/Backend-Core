from flask import jsonify
import zmq

def create(request):
    name = request['name']
    id = request['id']
    type = request['type']
    module = request['module']

    

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("ipc://backend.ipc")
    #socket.send_json({"name": name, "id": id, "type": type, "module": module})
    socket.send(f'POST;{name};{id};{type};{module}')

    #  Get the reply.
    message = socket.recv()
    if message == b'OK':
        return jsonify({"status": 200})
    else:
        return jsonify({"errors": [{"error": "", "message": "", "detail": ""}], "code": 400}) 

