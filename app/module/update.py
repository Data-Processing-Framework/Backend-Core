from flask import jsonify
import zmq


def update(request, moduleId):
    name = request['name']
    type = request['type']
    module = request['module']
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("ipc://backend.ipc")
    socket.send(f'{name};{type};{module};PUT;MODULE;{moduleId}')

    message = socket.recv()

    if message == '200':
        return jsonify({"status": 200})
    else:
        return jsonify({"errors": [{"error": "", "message": "", "detail": ""}], "code": 400}) 
