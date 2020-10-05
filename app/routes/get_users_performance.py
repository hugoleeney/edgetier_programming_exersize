import sqlalchemy
from sqlalchemy import text

from app import app, database, models
from app import app
from flask import jsonify

from sqlalchemy import inspect

# TODO: Give the route a name/path.
from app.models import Chat



@app.route("/users_performance", methods=["GET"])
def get_users_performance():
    """
    Return the interactions completed and average handling time of every user.
    :return: JSON array:

    [
        {
            "userId": 1,
            "name": "Test User",
            "chatsHandled": 10,
            "averageHandlingSeconds": 120
        },
        ...
    ]

    """

    # I chose not to use sqlalchemy models for this query because the sum of the datediff
    # is unfamiliar to me and could be messy because of SQL dialect differences.
    query = text("""SELECT chat.user_id, user.name, count(), sum(strftime('%s', chat.handle_end)-strftime('%s', chat.handle_start)) 
        FROM chat left join user on user.user_id=chat.user_id group by chat.user_id""")
    result = database.session.execute(query)
    chats_by_user = result.fetchall()

    returned = [{"userId":res[0], "name":res[1], "chatsHandled": res[2], "averageHandlingSeconds":res[3]/res[2]} for res in chats_by_user]
    return jsonify(returned)
