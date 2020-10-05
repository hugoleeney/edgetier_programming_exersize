import os

import fs

from app import app, models, database
from datetime import datetime
from http import HTTPStatus
from integrations import SavageRentals
from integrations.absolutely_class_airlines import AbsolutelyClassAirlines, FileInterface


@app.route("/chats/<int:chat_id>/end", methods=["POST"])
def end_chat(chat_id):
    """
    End a chat.
    :param chat_id: Requested user identifier.
    :return:        JSON object of the requested user.
    """

    # Record the time the chat was finished being handled.
    chat = models.Chat.query.get_or_404(chat_id)
    chat.handle_end = datetime.utcnow()
    database.session.commit()

    # Do something depending on the client. Note: the client is set in the .env file at the root.
    if os.environ['CLIENT_NAME'] == 'savage_rentals':
        savage_rentals = SavageRentals()
        savage_rentals.store_chat(chat)
    elif os.environ['CLIENT_NAME'] == 'absolutely_class_airlines':
        client = AbsolutelyClassAirlines('ACA', os.environ['CLIENT_NAME'], FileInterface(fs.open_fs('osfs://./')))
        client.store_chat(chat)

    return "", HTTPStatus.OK
