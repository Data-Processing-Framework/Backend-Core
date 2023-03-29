from threading import Lock, Thread
import zmq


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
                cls._instances[cls] = instance
        return cls._instances[cls]


class controller(metaclass=controllerMeta):
    value: str = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self) -> None:
        context = zmq.Context.instance()

        self.out = context.socket(zmq.PUB)
        self.out.bind("tcp://127.0.0.1:5557")
        self.response = context.socket(zmq.SUB)
        self.response.bind("tcp://127.0.0.1:5558")
        self.response.subscribe("")

    def send_message(self, message: str):
        self.out.send(message.encode("utf-8"))
        poller = zmq.Poller()
        poller.register(self.response, zmq.POLLIN)
        socket = poller.poll(timeout=10000)
        for a in socket:
            response = socket.recv_multipart()


c = controller()
c.send_message("hola")
print("a")
