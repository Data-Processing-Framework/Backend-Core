import pytest

from app import create_app
from dotenv import load_dotenv
from app.helpers.controller import controller

load_dotenv()


@pytest.fixture()
def app():
    app = create_app()
    controller()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here


    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()