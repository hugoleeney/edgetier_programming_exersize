from datetime import datetime
from http import HTTPStatus

from app import database
from app.models import User, Chat


df = '%Y%m%dT%H:%M:%S'


def test_get_user(client):
    """
    Test GET user route.
    :param client: Flask test client.
    """

    # Insert test users.
    user1 = User(name="Test User")
    user2 = User(name="Test User 2")
    database.session.add(user1)
    database.session.add(user2)
    database.session.commit()

    # Insert chats
    chats = [
        Chat(created=datetime.strptime("20201001T12:00:00", df), customer_name="asdf", user_id=user1.user_id,
                handle_start=datetime.strptime("20201001T12:00:01", df),
                handle_end=datetime.strptime("20201001T12:00:02", df)),
        Chat(created=datetime.strptime("20201001T12:00:00", df), customer_name="asdf", user_id=user1.user_id,
                handle_start=datetime.strptime("20201001T12:00:01", df),
                handle_end=datetime.strptime("20201001T12:00:02", df)),
        Chat(created=datetime.strptime("20201001T12:00:00", df), customer_name="asdf", user_id=user2.user_id,
                handle_start=datetime.strptime("20201001T12:01:00", df),
                handle_end=datetime.strptime("20201001T12:02:00", df)),
        Chat(created=datetime.strptime("20201001T12:00:00", df), customer_name="asdf", user_id=user2.user_id,
                handle_start=datetime.strptime("20201001T12:00:01", df),
                handle_end=datetime.strptime("20201011T12:00:02", df))
        ]
    for c in chats:
        database.session.add(c)
    database.session.commit()

    # Request the user.
    response = client.get(f"/users_performance")
    assert response.status_code == HTTPStatus.OK
    assert response.json[0] == {"userId": 1, "name": "Test User", "chatsHandled": 2, "averageHandlingSeconds": 1}
    assert response.json[1] == {"userId": 2, "name": "Test User 2", "chatsHandled": 2, "averageHandlingSeconds": (60+864001)/2}
