from threading import Lock, Thread
import zmq
import os
import json


class controllerMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                context = zmq.Context.instance()
                instance.request = context.socket(zmq.PUB)
                instance.request.bind(
                    "tcp://0.0.0.0:" + os.getenv("CONTROLLER_REQUEST_PORT")
                )
                instance.response = context.socket(zmq.SUB)
                instance.response.bind(
                    "tcp://0.0.0.0:" + os.getenv("CONTROLLER_RESPONSE_PORT")
                )
                instance.response.subscribe("")
                instance.n_workers = int(os.getenv("N_WORKERS")) + 1

                cls._instances[cls] = instance
        return cls._instances[cls]


class controller(metaclass=controllerMeta):
    def poll_workers(self):
        self.request.send()

    def send_message(self, message: str):
        self.request.send_string(message)
        n_workers = self.n_workers
        poller = zmq.Poller()
        poller.register(self.response, zmq.POLLIN)
        errors = []
        response = []
        while n_workers > 0:
            try:
                socket = dict(poller.poll(timeout=10000))
                if self.response in socket:
                    res = self.response.recv_string()
                    if res != "OK" and message != "STATUS":
                        errors.append(json.loads(res))
                    if message == "STATUS" and "status" in res:
                        response.append(json.loads(res))
                    elif message == "STATUS":
                        errors.append(json.loads(res))
                    n_workers -= 1
                if socket == {}:
                    n_workers = 0
                    errors.append(
                        {
                            "error": "Core error",
                            "message": "Couldn't connect to all workers.",
                            "detail": "Please restart all containers and try again.",
                        }
                    )
            except zmq.ZMQError as e:
                errors.append(
                    {
                        "errors": [
                            {
                                "error": "Core error",
                                "message": str(e),
                                "detail": "Please restart the system and try again.",
                            }
                        ],
                        "code": 400,
                    }
                )

        if errors:
            return {"errors": errors, "code": 400}
        elif response:
            return {"response": response, "code": 200}
        else:
            return {"code": 200}


# TODO create tests with this info


def test_singleton(instance_name: str) -> None:
    singleton = controller()
    for a in singleton.send_message("Funciona!"):
        print("singleton: " + str(instance_name) + " - " + a)


if __name__ == "__main__":
    # The client code.

    print(
        "If you see the same value, then singleton was reused (yay!)\n"
        "If you see different values, "
        "then 2 singletons were created (booo!!)\n\n"
        "RESULT:\n"
    )

    process1 = Thread(target=test_singleton, args=(1,))
    process2 = Thread(target=test_singleton, args=(2,))
    process1.start()
    process2.start()
