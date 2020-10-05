import json
import os
from http import HTTPStatus

import fs
import pytest
import responses
from datetime import datetime, timedelta

from app import database
from app.models import Chat, Message, User
from integrations import SavageRentals
from integrations.absolutely_class_airlines import AbsolutelyClassAirlines, FileInterface, CouldntObtainFileHandle
from integrations.savage_rentals import URL


def dummy_open(*a, **kw):
    raise fs.errors.FileExists("asdf")


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

    inmemfs = fs.open_fs('mem://')

    savage_rentals = AbsolutelyClassAirlines("edgetier_chats", 'absolutely_class_airlines', FileInterface(inmemfs))
    savage_rentals.store_chat(chat)

    file_path = os.path.join("edgetier_chats", 'absolutely_class_airlines', "1.txt")
    assert inmemfs.exists(file_path) == True
    contents = inmemfs.open(file_path, 'r').read()
    assert contents.split('\n') == [
        'Chat on 01 Jan 2020 14:55:',
        '',
        '[14:55, Customer]: Hello',
        '[14:56, Agent]: Hi, please let me know how I can help',
        "This chat took 300 seconds to handle."
    ]


@pytest.mark.freeze_time("2020-01-01 15:00:00")
@responses.activate
def test_store_chat_couldnt_obtain_file_handle(test_database):

    now = datetime.utcnow()
    user = User(name="Test Agent")
    chat = Chat(
        created=now - timedelta(minutes=10),
        customer_name="John",
        handle_start=now - timedelta(minutes=5),
        handle_end=now,
        user_id=user.user_id,
        messages=[]
    )

    inmemfs = fs.open_fs('mem://')
    inmemfs.open = dummy_open

    savage_rentals = AbsolutelyClassAirlines("edgetier_chats", 'absolutely_class_airlines', FileInterface(inmemfs))
    with pytest.raises(CouldntObtainFileHandle):
        savage_rentals.store_chat(chat)
