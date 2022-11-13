import pytest

from availapi import app


@pytest.fixture()
def app_fixture():
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app_fixture):
    return app_fixture.test_client()
