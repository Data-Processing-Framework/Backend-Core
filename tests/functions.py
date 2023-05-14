import os
import time
from app.helpers.file_locker import block_write, block_write_file

def file_exists(file_name: str, path: str) -> bool:
    if file_name not in os.listdir(path):
        return False
    return True


def remove_size(file_name):
    os.popen(f"cp ./app/data/{file_name} ./app/data/provisional.json")
    time.sleep(3)
    with open(f"./app/data/{file_name}", "w") as f:
        f.truncate(0)


def return_size(file_name):
    os.popen(f"cp ./app/data/provisional.json ./app/data/{file_name}")
    time.sleep(3)
    os.remove("./app/data/provisional.json")
