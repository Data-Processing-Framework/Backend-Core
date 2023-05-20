from threading import Lock, Thread
import zmq
import os
import json


class controllerMeta(type):
    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                context = zmq.Context.instance()
                instance.request = context.socket(zmq.PUB)
                instance.request.bind(
                    "tcp://0.0.0.0:" + os.getenv("CONTROLLER_REQUEST_PORT")
                )
                instance.status_bus = context.socket(zmq.SUB)
                instance.status_bus.bind(
                    "tcp://0.0.0.0:" + os.getenv("CONTROLLER_STATUS_PORT")
                )
                instance.status_bus.subscribe("")
                instance.n_workers = int(os.getenv("N_WORKERS")) + 1

                Thread(target=instance.status).start()

                cls._instances[cls] = instance
        return cls._instances[cls]


class controller(metaclass=controllerMeta):
    system_status = {}
    status_bus = None
    request = None

    def send_message(self, message: str):
        try:
            if message == "STATUS":
                return {"code": 200, "response": self.system_status}
            self.request.send_string(message)
            return {"code": 200}

        except Exception as e:
            return {
                "errors": [
                    {
                        "error": "Core error",
                        "message": str(e),
                        "detail": "Please restart the system and try again.",
                    }
                ],
                "code": 400,
            }

    def status(self):
        poller = zmq.Poller()
        poller.register(self.status_bus, zmq.POLLIN)
        self.system_status["proba"] = 0
        while True:
            try:
                socket = dict(poller.poll(timeout=10000))
                if self.status_bus in socket:
                    res = json.loads(self.status_bus.recv_string())
                    self.system_status[res["id"]] = res
                else:
                    self.request.send_string("STATUS")

            except Exception as e:
                continue