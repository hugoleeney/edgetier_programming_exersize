# EdgeTier Python Challenge

**Note:** Please do not put your solution in a public repository (GitHub etc.). We are sending this to multiple candidates and do not want anyone to have an unfair advantage.

# Description

EdgeTier's main product, Arthur, allows contact centre agents to answer customer queries via live chat and email. This project contains a tiny subset of the system with a database of users, chats, and chat messages. 

# Application 

The application uses [Flask](https://flask.palletsprojects.com/en/1.1.x/) with [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/). There is an in-memory SQLite database automatically created and populated with some data every time the application starts. The database tables are defined in `/app/models.py`. The data can be seen in `/configuration/insert_data.py` (and at the bottom of this page for ease of reference).

`/app/routes/get_user.py` has been provided as an example as a finished route with tests in `/test/test_app/test_get_user.py` to help. For those with no experience of SQLAlchemy, you can just write raw SQL if you prefer and `/app/get_user.py` has an example of how to do that. 

## Setup

* Install Python 3.6+.
* Install SQLite. Mac already has this installed already most of the time.
* `git clone` the repository.

### Run With PyCharm

1. Open the project, select your Project Interpreter from preferences and install all packages from `requirements.txt`.
1. Create a new run configuration ("Edit Configurations..." at the top right).
2. Set the "script path" to your virtual environment's `bin/flask`.
3. In "parameters" type "run".

You should now be able to run `main.py`. Go to http://localhost:5000/users/1 to confirm it's running.

### Run With Command Line

1. Create and activate a new virtual environment.
2. `pip install requirements.txt`.
3. `flask run`.

Go to http://localhost:5000/users/1 to confirm it's running.

## Tests

There are some sample tests in `/test` written using [pytest](https://docs.pytest.org/en/stable/). 

### Run Tests With PyCharm

1. Create a new configuration selecting pytest from the "Templates".
2. See the root of the project as the working directory if it's not already.

You should now be able to run the tests.

### Run Tests With Command Line

1. Activate your virtual environment. 
2. `pytest test` to run all tests.

# Tasks

## Task 1

Managers in contact centres like to see statistics on agents' performance. A blank route has been created (see `/app/routes/get_users_performance.py`) that needs to completed. Calculate and return the total number of chats handled and the average handling time for all users in the database. We also haven't decided yet what the route should be called so you will need to give it a name (and rename the file if you prefer).

## Task 2

Arthur integrates with our client's systems to extract data to help agents answer queries and sometimes store information like the transcript from a chat. Imagine Arthur was built for one customer called Savage Rentals and EdgeTier has just signed their second customer, Absolutely Class Airlines. Some parts of the system need to be modified as the second client has some new requirements. 

Savage Rentals have a record of each chat posted to their API when an agent finishes it. This code exists already in `/integrations` and is called in `/app/routes/end_chat.py`. But the new customer, Absolutely Class Airlines has some new requirements: 

* Each chat should be written to a directory (call the directory whatever you like).  
* They want the chat written in the same exact same format as Savage Rentals but with one new line added to the end of each transcript containing the text "This chat took ??? seconds to handle." (with ??? being the handling time).
* Each customer should get a new directory based on their name (there's a `customer_name` column in the chat table).
* The name of each file should increment for each customer.

Example, with Customer A and Customer B, you might end up with something like this:

```
output
  ├─┬ customer-a
  │ ├── 1.txt
  │ └── 2.txt
  └─┬ customer-b
    ├── 1.txt
    ├── 2.txt
    └── 3.txt
```

Feel free to modify `end_chat.py` and anything in the `/integrations` directory, including existing code. 

# Submission

Please complete the challenge and either send us a link to a private repository on BitBucket/GitHub etc. Or zip and email your solution.

# Data

## Users

```
+-------------------+
|user_id|name       |
+-------------------+
|1      |Test User 1|
|2      |Test User 2|
|3      |Test User 3|
+-------------------+
```

## Chats

```
+--------------------------------------------------------------------------------------------------------------+
|chat_id|created                   |customer_name|user_id|handle_start              |handle_end                |
+--------------------------------------------------------------------------------------------------------------+
|1      |2020-09-29 08:55:20.540957|John         |1      |2020-09-29 09:00:20.540957|2020-09-29 09:05:20.540957|
|2      |2020-09-29 09:00:20.540957|Jane         |1      |2020-09-29 09:02:20.540957|                          |
|3      |2020-09-29 09:00:20.540957|Jerry        |3      |2020-09-29 09:02:20.540957|2020-09-29 09:05:20.540957|
|4      |2020-09-29 08:40:20.540957|Jacintha     |3      |2020-09-29 08:44:20.540957|2020-09-29 08:54:20.540957|
|5      |2020-09-29 08:55:20.540957|Julia        |       |                          |                          |
|6      |2020-09-29 08:50:20.540957|Joseph       |       |                          |                          |
+--------------------------------------------------------------------------------------------------------------+
```

## Messages

```
+-------------------------------------------------------------------------------------------------+
|message_id|chat_id    |text                                   |user_id|sent_at                   |
+-------------------------------------------------------------------------------------------------+
|1         |1          |Hello, I need to cancel my reservation.|       |2020-09-29 09:00:20.540957|
|2         |1          |I can do that.                         |1      |2020-09-29 09:01:20.540957|
|3         |1          |That has been cancelled.               |1      |2020-09-29 09:02:20.540957|
|4         |1          |Sound, thanks.                         |       |2020-09-29 09:04:20.540957|
|5         |2          |Your website is giving me an error.    |       |2020-09-29 09:02:20.540957|
|6         |2          |Sorry to hear that, what is the error? |1      |2020-09-29 09:04:20.540957|
|7         |3          |What are your opening hours?.          |       |2020-09-29 09:02:20.540957|
|8         |3          |Monday to Friday, 9am to 6pm.          |3      |2020-09-29 09:04:20.540957|
|9         |3          |Thanks.                                |       |2020-09-29 09:04:20.540957|
|10        |4          |I'd like to make a complaint.          |       |2020-09-29 08:44:20.540957|
|11        |4          |Please fill out a complaint form.      |3      |2020-09-29 08:46:20.540957|
|12        |4          |You can find it on our website.        |3      |2020-09-29 08:53:20.540957|
|13        |4          |OK I'll do that.                       |       |2020-09-29 09:01:20.540957|
+-------------------------------------------------------------------------------------------------+
```