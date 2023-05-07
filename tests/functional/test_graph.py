from tests.functions import *
import pytest
import time


@pytest.mark.parametrize("code, value, json, error",  [
    (400, False, [], "Couldn't connect to all workers."),
    (400, True, [], "File Empty")
])
def test_graph_put(client, code, value, json, error):
    if value:
        remove_size("graph.json")
    response = client.put("/graph/", json=json)
    assert response.status_code == code
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
    response = client.get("/graph/")
    assert response.status_code == code

    if value:
        return_size("graph.json")
    time.sleep(3)
