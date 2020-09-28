from pytest import fixture

from app import app, database


@fixture(scope='function')
def test_database():
    """
    Set up the database.
    """
    database.drop_all()
    database.create_all()
    yield database
    database.drop_all()


@fixture(scope='function')
def client(test_database):
    """
    Create a Flask test client.
    """
    app.testing = True
    yield app.test_client()
