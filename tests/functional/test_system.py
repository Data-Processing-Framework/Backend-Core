from tests.functions import *
import pytest
import time


def test_system_start(client):
    time.sleep(5)
    response = client.get('/system/start')
    assert response.status_code == 200
    time.sleep(5)

def test_system_stop(client):
    time.sleep(5)
    response = client.get('/system/stop')
    assert response.status_code == 200
    time.sleep(5)

def test_system_restart(client):
    time.sleep(5)
    client.get('/system/start')
    response = client.get('/system/restart')
    assert response.status_code == 200
    time.sleep(5)

def test_system_status(client):
    time.sleep(5)
    response = client.get('/system/status')
    assert response.status_code == 200
    time.sleep(5)