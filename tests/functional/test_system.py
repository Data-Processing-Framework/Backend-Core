from tests.functions import *
import pytest
import time


def test_system_status(client):
    time.sleep(15)
    response = client.get('/system/status')
    assert response.status_code == 200
    assert response.json["response"]["worker-input"]["status"] == "RESTARTING"
    assert response.json["response"][str(list(response.json["response"].keys())[0])]["status"] == "RUNNING"
    time.sleep(15)


def test_system_restart(client):
    time.sleep(15)

    response = client.get('/system/restart')
    assert response.status_code == 200

    res = client.get('/system/status')
    while res.json["response"][str(list(res.json["response"].keys())[0])]["status"] == "RESTARTING":
        time.sleep(1)
        res = client.get('/system/status')

    time.sleep(15)


def test_system_stop(client):
    time.sleep(15)
    response = client.get('/system/stop')
    
    assert response.status_code == 200

    while True:
        status_res = client.get('/system/status')
        while "response" not in list(status_res.json.keys()):
            status_res = client.get('/system/status')
            time.sleep(1)
        status = status_res.json["response"][str(list(status_res.json["response"].keys())[0])]["status"]
        if status != "RUNNING":
            break
        else:
            time.sleep(5)

    assert status == "STOPPED"
    time.sleep(15)


def test_system_start(client):
    time.sleep(15)
    response = client.get('/system/start')

    assert response.status_code == 200

    while True:
        status_res = client.get('/system/status')
        while "response" not in list(status_res.json.keys()):
            status_res = client.get('/system/status')
            time.sleep(1)
        status = status_res.json["response"][str(list(status_res.json["response"].keys())[0])]["status"]
        if status != "STOPPED":
            break

    assert status == "RUNNING"
    assert status_res.status_code == 200
    time.sleep(15)
