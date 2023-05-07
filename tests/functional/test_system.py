from tests.functions import *
import pytest
import time


def test_system_start(client):
    response = client.get('/system/start')
    assert response.status_code == 200
    time.sleep(3)

def test_system_stop(client):
    response = client.get('/system/stop')
    assert response.status_code == 200
    time.sleep(3)

def test_system_restart(client):
    client.get('/system/start')
    response = client.get('/system/restart')
    assert response.status_code == 200
    time.sleep(3)

def test_system_status(client):
    response = client.get('/system/status')
    assert response.status_code == 200
    time.sleep(3)