from tests.functions import *
import pytest
import time


def test_system_status(client):
    time.sleep(5)
    response = client.get('/system/status')
    assert response.status_code == 200
    assert response.json["response"][0]["status"] == "RUNNING"

    time.sleep(15)


def test_system_restart(client):
    time.sleep(5)

    response = client.get('/system/restart')
    assert response.status_code == 200

    res = client.get('/system/status')
    while res.json["response"][0]["status"] == "RESTARTING":
        time.sleep(1)
        res = client.get('/system/status')

    time.sleep(15)


def test_system_stop(client):
    time.sleep(15)
    response = client.get('/system/stop')
    res = client.get('/system/status')
    assert response.status_code == 200
    assert res.json["response"][0]["status"] == "STOPPED"
    time.sleep(15)


def test_system_start(client):
    time.sleep(15)
    response = client.get('/system/start')
    res = client.get('/system/status')
    assert response.status_code == 200
    assert res.json["response"][0]["status"] == "RUNNING"
    time.sleep(15)
