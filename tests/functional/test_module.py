from tests.functions import *
import pytest
import time


@pytest.mark.parametrize("route, json, file_name, path, expected",  [
    ('/module/',
     {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     "./app/data/modules/",
     [400, True, "Couldn't connect to all workers."]),
    ('/module/',
     {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     "./app/data/modules/",
     [400, True, "Module with the same name already exists"]),
    ('/module/',
     {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova2.py",
     "./app/data/modules/",
     [400, True, "Couldn't connect to all workers."])
])
def test_module_post(client, route, json, file_name, path, expected):
    response = client.post(route, json=json)
    assert response.status_code == expected[0] # Provisional 400 -> 200
    assert file_exists(file_name, path) == expected[1]
    assert response.json["errors"][0]["message"] == expected[2]
    time.sleep(5)


@pytest.mark.parametrize("route, json, file_name, path, expected, extra",  [
    ('/module/prova',
     {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     "./app/data/modules/",
     [400, False, "Couldn't connect to all workers."], False),
    ('/module/dale',
     {"name": "dale", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "dale.py",
     "./app/data/modules/",
     [400, False, "Module does not exist"], False),
    ('/module/dale',
     {"name": "dale", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "dale.py",
     "./app/data/modules/",
     [400, False, "File Empty"], True)
])
def test_module_delete(client, route, json, file_name, path, expected, extra):
    if extra:
        remove_size("modules.json")

    response = client.delete(route, json=json)
    assert response.status_code == expected[0] # Provisional 400 -> 200
    assert file_exists(file_name, path) == expected[1]
    assert response.json["errors"][0]["message"] == expected[2]

    if extra:
        return_size("modules.json")
    time.sleep(2)


@pytest.mark.parametrize("route, json, file_name, path, expected, error, extra",  [
    ('/module/prova',
     {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     "./app/data/modules/",
     [400, False, "Module does not exist"],
      True, False),
    ('/module/Julio',
     {"name": "Julio", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "Julio.py",
     "./app/data/modules/",
     [400, True], 
     False, False),
    ('/module/Julio',
     {"name": "Julio", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "Julio.py",
     "./app/data/modules/",
     [400, True, "File Empty"], 
     False, True)
])
def test_module_put(client, route, json, file_name, path, expected, error, extra):
    if extra:
        remove_size("modules.json")

    response = client.put(route, json=json)
    assert response.status_code == expected[0] # Provisional 400 -> 200
    assert file_exists(file_name, path) == expected[1]
    if error:
        assert response.json["errors"][0]["message"] == expected[2]

    if extra:
        return_size("modules.json")
    time.sleep(2)


@pytest.mark.parametrize("route, json, file_name, path, expected, error, extra",  [
    ('/module/Julio',
     {'code': 'class Module():\n    def __init__(self):\n       pass', 'description': 'Text Input module', 'name': 'Julio', 'type': 'Input', 'type_in': ['str', 'JSON'], 'type_out': ['str']},
     "Julio.py",
     "./app/data/modules/",
     [200, True],
     False, False),
    ('/module/prova',
     {'code': 'class Module():\n    def __init__(self):\n       pass', 'description': 'Text Input module', 'name': 'Julio', 'type': 'Input', 'type_in': ['str', 'JSON'], 'type_out': ['str']},
     "prova.py",
     "./app/data/modules/",
     [400, False, "Module does not exist"],
     True, False),
    ('/module/prova',
     {'code': 'class Module():\n    def __init__(self):\n       pass', 'description': 'Text Input module', 'name': 'Julio', 'type': 'Input', 'type_in': ['str', 'JSON'], 'type_out': ['str']},
     "prova.py",
     "./app/data/modules/",
     [400, False, "File Empty"],
     True, True)
])
def test_module_get(client, route, json, file_name, path, expected, error, extra):
    if extra:
        remove_size("modules.json")

    response = client.get(route)
    assert response.status_code == expected[0] # Provisional 400 -> 200
    assert file_exists(file_name, path) == expected[1]
    if error:
        assert response.json["errors"][0]["message"] == expected[2]
    else:
        assert response.json == json

    if extra:
        return_size("modules.json")
    time.sleep(2)
