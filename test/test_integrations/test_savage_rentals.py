import json
from http import HTTPStatus

import pytest
import responses
from datetime import datetime, timedelta

from app import database
from app.models import Chat, Message, User
from integrations import SavageRentals
from integrations.savage_rentals import URL


@pytest.mark.freeze_time("2020-01-01 15:00:00")
@responses.activate
def test_store_chat(test_database):
    """
    Send a chat to Savage Rental's CRM.
    :param test_database: Fixture creating a test database.
    """

    # Mock API requests.
    responses.add(responses.POST, URL, status=HTTPStatus.OK)

    now = datetime.utcnow()

    user = User(name="Test Agent")
    database.session.add(user)
    database.session.flush()

    # Insert a test chat.
    chat = Chat(
        created=now - timedelta(minutes=10),
        customer_name="John",
        handle_start=now - timedelta(minutes=5),
        handle_end=now,
        user_id=user.user_id,
        messages=[
            Message(
                text='Hello',
                sent_at=now - timedelta(minutes=5)
            ),
            Message(
                text='Hi, please let me know how I can help',
                sent_at=now - timedelta(minutes=4),
                user_id=user.user_id,
            )
        ]
    )

    database.session.add(chat)
    database.session.commit()

    savage_rentals = SavageRentals()
    savage_rentals.store_chat(chat)

    assert responses.calls[0].request.url == URL

    post_data = json.loads(responses.calls[0].request.body.decode('utf-8'))
    assert post_data["content"].split('\n') == [
        'Chat on 01 Jan 2020 14:55:',
        '',
        '[14:55, Customer]: Hello',
        '[14:56, Agent]: Hi, please let me know how I can help'
    ]
