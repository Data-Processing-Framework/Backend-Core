import json
import os
import fcntl

def block_read(filename):
    actualfile = open(filename, "r")
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_SH)
    modules = json.load(actualfile)
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_UN)
    return modules

def block_write(filename, data):
    actualfile = open(filename, "w")
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_EX)
    actualfile.write(data)
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_UN)


def block_delete(filename):
    actualfile = open(filename, "w+")
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_EX)
    actualfile.close()
    os.remove(filename)
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_UN)