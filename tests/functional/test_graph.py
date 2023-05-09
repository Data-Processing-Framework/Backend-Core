from tests.functions import *
import pytest
import time


@pytest.mark.parametrize("code, value, error",  [
    (200, False, ""),
    (400, True, "File Empty")
])
def test_graph_put(client, code, value, error):
    if value:
        remove_size("graph.json")
    time.sleep(5)
    response = client.put("/graph/", json=[{"name": "Input1", "type": "Input", "module": "dummyInput", "inputs": [], "position": []}, {"name": "Transform1", "type": "Transform", "module": "dummyTransform", "inputs": ["Input1"], "position": []}])
    assert response.status_code == code

    if error != "":
        assert response.json["errors"][0]["message"] == error

    if value:
        return_size("graph.json")
    time.sleep(5)

@pytest.mark.parametrize("code, value",  [
    (200, False),
    (400, True)
])
def test_graph_get(client, code, value):
    if value:
        remove_size("graph.json")
    time.sleep(5)
    response = client.get("/graph/")
    assert response.status_code == code

    if value:
        return_size("graph.json")
    time.sleep(5)
