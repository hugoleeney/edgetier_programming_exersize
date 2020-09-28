import requests

URL = "https://savage-rentals-fake-address.com/"


class SavageRentals:
    """
    Connect to Savage Rental's CRM.
    """
    def store_chat(self, chat):
        """
        Create and store a transcript of a chat in the CRM.
        :param chat: Chat to store.
        """
        time = chat.handle_start.strftime("%d %b %Y %H:%M")
        opening = f'Chat on {time}:\n\n'
        messages = '\n'.join([self._format_message(message) for message in chat.messages])
        content = opening + messages

        try:
            requests.post(URL, json={"content": content})
        except (ConnectionError, Exception):
            pass

    @staticmethod
    def _format_message(message):
        """
        Make a description of a message.
        :param message: Chat message.
        :return:        String for a chat message in the format of "[16:00, Agent]: Hello".
        """
        sender = 'Agent' if isinstance(message.user_id, int) else 'Customer'
        time = message.sent_at.strftime("%H:%M")
        return f'[{time}, {sender}]: {message.text}'
