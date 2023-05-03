def test_module_post(client):
    response = client.post('/module', json={"name": "Prova", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"})
    assert response.status_code == 200

def test_module_post_error(client):
  
    response = client.post('/module', json={"name": "Prova"})
    assert response.status_code == 400

def test_module_get(client):  
    response = client.get('/module')
    assert response.status_code == 200

def test_module_get_id(client):  
    client.post('/module', json={"name": "test", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"})
    response = client.get('/module/test')
    assert response.status_code == 200

def test_module_get_id_error(client):  
    response = client.get('/module/test')
    assert response.status_code == 400

def test_module_delete(client):  
    client.post('/module', json={"name": "test", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"})
    response = client.delete('/module/test')
    assert response.status_code == 200

def test_module_delete_error(client):  
    response = client.delete('/module/test')
    assert response.status_code == 400

def test_module_put(client):  
    client.post('/module', json={"name": "test", "type": "Input", "description": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"})
    response = client.put('/module/test', json={"name": "test", "type": "Input", "description2": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"})
    assert response.status_code == 200

def test_module_put_error(client):  
    response = client.put('/module/test', json={"name": "test", "type": "Input", "description2": "Text Input module", "type_in": ["str","JSON"], "type_out": ["str"], "code": "class Module():\n    def __init__(self):\n       pass"})
    assert response.status_code == 400