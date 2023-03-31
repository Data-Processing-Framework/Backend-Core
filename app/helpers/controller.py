from threading import Lock, Thread
import zmq
from dotenv import load_dotenv
import os

load_dotenv()


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
                instance.request.bind(os.getenv("request_bus_address"))
                instance.response = context.socket(zmq.SUB)
                instance.response.bind(os.getenv("response_bus_address"))
                instance.response.subscribe("")
                instance.n_workers = int(os.getenv("n_workers"))

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
        while n_workers > 0:
            try:
                socket = dict(poller.poll(timeout=1000))
                if self.response in socket:
                    yield self.response.recv_string()
                    n_workers -= 1
                if socket == {}:
                    n_workers = 0
            except zmq.ZMQError as e:
                yield {}


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
