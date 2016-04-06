DukeDS Handover Service
=======================

Web service to facilitate notification and transfer of projects in DukeDS

Installation - Local
====================

1. Clone the repository
2. Install dependencies

        pip install -r requirements.txt

3. Create a `settings.py` file:

        cp handoverservice/settings.template handoverservice/settings.py

4. Edit the `settings.py` file to populate the `DDSCLIENT_PROPERTIES` with a the DukeDS API URL and a software agent key, e.g.

        DDSCLIENT_PROPERTIES = {
          'url': 'https://uatest.dataservice.duke.edu/api/v1',
          'agent_key': '37a9cc3b5ed69bc96081e98478c009bb',
        }

5. Create the database schema:

        $ python manage.py migrate

6. Create a superuser (A user account is required for making authenticated API requests)

        $ python manage.py createsuperuser

6. Start the app:

        $ python manage.py runserver

7. The server is running and the API can be explored at [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)


Installation - Docker Compose
=============================

1. Clone the repository
2. Create a `handoverservice.env` file

        cp handoverservice.env.sample handoverservice.env

3. Edit the `handoverservice.env` file to populate the your DukeDS API details, a django key, and a database username/password to use:

        HANDOVERSERVICE_SECRET_KEY=some-random-string
        HANDOVERSERVICE_DDSCLIENT_URL=https://dataservice-host/api/v1
        HANDOVERSERVICE_DDSCLIENT_AGENT_KEY=your-agent-key
        POSTGRES_USER=handover_user
        POSTGRES_PASSWORD=some-random-password
        POSTGRES_DB=handover

4. Create the database schema:

        $ docker-compose run web python manage.py migrate

5. Create a superuser (A user account is required for making authenticated API requests)

        $ docker-compose run web python manage.py createsuperuser

6. Start the app:

        $ docker-compose up

7. The server is running and the API can be explored at  [http://your-docker-host:8000/api/v1/](http://your-docker-host:8000/api/v1/)


Usage
=====

## Register a DukeDS user

The Handover Service communicates with the Duke Data Service API as a software agent. For this to work, DukeDS users must register their UDID and user key in the handover service. This can be done from the admin interface:

1. Visit http://127.0.0.1:8000/admin/handover_api/dukedsuser/
2. Login with your superuser account
3. Click **Add Duke DS User**
  1. Select or add a User (e.g. the superuser you created)
  2. Enter the DukeDS UDID of the user and the user's API key
  3. Click **Save**

## Get a token for authentication

The API requires authentication. To avoid sending username and password in every request, you generate a token for API authentication.

1. Visit http://127.0.0.1:8000/admin/authtoken/token/
2. Click **Add Token**
4. Select your the user account and click **Save**
5. Note the token (e.g. `4a9a367a161d3b2315da17f3f44eaaaf5146b5a2`)

## Sending a Draft

The term draft is used to refer to a project that is about to be handed over from a sender to a receiver. The sender is expected to use the [DukeDSClient](https://github.com/Duke-GCB/DukeDSClient) to create and upload a project. Prior to review/acceptance by the receiver, it is in a "draft" state. The Handover service can send an email to the receiver, notifying them the data in the project is ready for their review.


1. Create a Draft:

        $ curl -X POST \
          -H "Authorization: Token <your-token>"
          -H "Content-Type: application/json" \
          -d '{"project_id": "project-dds-uuid", "from_user_id": "from-user-uuid", "to_user_id": "to-user-uuid"}' \
          http://127.0.0.1:8000/api/v1/drafts/
          {"id":1,"url":"http://127.0.0.1:8000/api/v1/drafts/1/","project_id":"xxxx","from_user_id":"xxxx","to_user_id":"xxxx","state":0}

2. Send the email (**Without changing settings.py to activate a real email backend, emails will only be printed to the django console**)

        $ curl -X POST http://127.0.0.1:8000/api/v1/drafts/1/send/
            {"id":1,"url":"http://127.0.0.1:8000/api/v1/drafts/1/","project_id":"xxxx","from_user_id":"xxxx","to_user_id":"xxxx","state":1}

Notice the state change, and the running django server should print out the email to the console
