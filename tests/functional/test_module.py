from tests.functions import *
import pytest
import time


@pytest.mark.parametrize("json, file_name, expected",  [
    ({"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     [200, True]),
    ({"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     [400, True, "Module with the same name already exists"]),
    ({"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova2.py",
     [200, True]),
    ({"name": "prova", "type": "Input", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     [400, True, "The field 'description' is missing from the JSON"]),
])
def test_module_post(client, json, file_name, expected):
    time.sleep(5)
    res = client.get('/system/status')

    while res.json["response"][0]["status"] != "RUNNING":
        time.sleep(1)
        res = client.get('/system/status')
    
    response = client.post("/module/", json=json)

    assert response.status_code == expected[0]
    assert file_exists(file_name, "./app/data/modules/") == expected[1]

    if len(expected) > 2:
        assert response.json["errors"][0]["message"] == expected[2]

    res = client.get('/system/status')
    while res.json["response"][0]["status"] == "RESTARTING":
        time.sleep(1)
        res = client.get('/system/status')

    time.sleep(5)


@pytest.mark.parametrize("route, json, file_name, path, expected, extra",  [
    ('/module/prova',
     {"name": "prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     "./app/data/modules/",
     [200, False], False),
    ('/module/prova2',
     {"name": "prova2", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova2.py",
     "./app/data/modules/",
     [200, False], False),
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

    time.sleep(5)

    response = client.delete(route, json=json)

    assert response.status_code == expected[0]
    assert file_exists(file_name, path) == expected[1]

    if len(expected) > 2:
        assert response.json["errors"][0]["message"] == expected[2]

    if extra:
        return_size("modules.json")

    res = client.get('/system/status')
    while res.json["response"][0]["status"] == "RESTARTING":
        time.sleep(1)
        res = client.get('/system/status')


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
     [200, True], 
     False, False),
    ('/module/Julio',
     {"name": "Julio", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "Julio.py",
     "./app/data/modules/",
     [400, True, "File Empty"], 
     False, True),
    ('/module/prova',
     {"name": "prova", "type": "Input", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"},
     "prova.py",
     "./app/data/modules/",
     [400, False, "The field 'description' is missing from the JSON"],
      True, False)
])
def test_module_put(client, route, json, file_name, path, expected, error, extra):
    if extra:
        remove_size("modules.json")

    time.sleep(5)

    response = client.put(route, json=json)

    assert response.status_code == expected[0]
    assert file_exists(file_name, path) == expected[1]

    if error:
        assert response.json["errors"][0]["message"] == expected[2]

    if extra:
        return_size("modules.json")

    res = client.get('/system/status')
    while res.json["response"][0]["status"] == "RESTARTING":
        time.sleep(1)
        res = client.get('/system/status')


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

    time.sleep(5)

    response = client.get(route)

    assert response.status_code == expected[0]
    assert file_exists(file_name, path) == expected[1]

    if error:
        assert response.json["errors"][0]["message"] == expected[2]
    else:
        assert response.json == json

    if extra:
        return_size("modules.json")

    time.sleep(5)
