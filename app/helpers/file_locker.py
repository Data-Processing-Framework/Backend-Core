import json
import os
import fcntl
from time import sleep

def block_read(filename):
    actualfile = open(filename, "r")
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_SH)
    modules = json.load(actualfile)
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_UN)
    return modules

def block_write(filename, data):
    actualfile = open(filename, "w+")
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_EX)
    json.dump(data, actualfile, indent=4)
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_UN)

def block_write_file(filename, data):
    actualfile = open(filename, "w+")
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_EX)
    actualfile.write(data)
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_UN)

def block_delete(filename):
    actualfile = open(filename, "w+")
    fcntl.flock(actualfile.fileno(), fcntl.LOCK_EX)
    actualfile.close()
    os.remove(filename)
    #fcntl.flock(actualfile.fileno(), fcntl.LOCK_UN)
