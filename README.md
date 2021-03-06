D4S2: Data Delivery Service
==================================

Web service to facilitate notification and transfer of projects in Duke Data Service and S3 Object Stores.

[![CircleCI](https://circleci.com/gh/Duke-GCB/D4S2.svg?style=svg)](https://circleci.com/gh/Duke-GCB/D4S2)

Installation - Local Development
================================

This application uses postgres-specific features, so you'll need a postgres server. Alternatively, you can use the docker-compose method.

1. Clone the repository
2. Install dependencies

        pip install -r requirements.txt

3. Create a `settings.py` file, providing your database credetnials:

        cp d4s2/settings_test.py d4s2/settings.py

4. Create the database schema:

        $ python manage.py migrate

5. Create a superuser (A user account is required for making authenticated API requests)

        $ python manage.py createsuperuser

6 . Register an application with a Duke DS instance and create a DDSEndpoint with the URLs, agent key, and provider id

        $ python manage.py createddsendpoint \
          endpoint-name \
          https://api.dataservice.duke.edu/api/v1 \
          registered-application-agent-key \
          https://dataservice.duke.edu \
          openid-provider-id

7. Start the app:

        $ python manage.py runserver

8. Start the background task runner:

        $ python manage.py process_tasks

9. The server is running and the API can be explored at [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)


Installation - Docker Compose Development
=========================================

1. Clone the repository
2. Create a `d4s2.dev.env` file

        cp d4s2.sample.env d4s2.dev.env

3. Edit your `d4s2.dev.env` file to provide runtime details:

        D4S2_ALLOWED_HOST=*
        D4S2_SECRET_KEY=some-random-string
        D4S2_DDSCLIENT_URL=https://dataservice.host.com/api/v1
        D4S2_DDSCLIENT_PORTAL_ROOT=https://dataservice.host.com/
        D4S2_DDSCLIENT_AGENT_KEY=agent-key-from-duke-ds
        D4S2_DDSCLIENT_OPENID_PROVIDER_ID=provider-id-from-dds-openid-provider
        D4S2_SMTP_HOST=smtp.host.com
        POSTGRES_USER=d4s2_user
        POSTGRES_PASSWORD=newly-generated-password
        POSTGRES_DB=d4s2_db
        POSTGRES_HOST=db

4. Build the application's docker image:

        $ docker-compose -f docker-compose.dev.yml build

5. Create a superuser (A user account is required for making authenticated API requests)

        $ docker-compose -f docker-compose.dev.yml run web python manage.py createsuperuser

6. Start the app:

        $ docker-compose -f docker-compose.dev.yml up

7. The server is running and the API can be explored at  [http://your-docker-host:8000/api//](http://your-docker-host:8000/api/v1/)

Deployment
==========

We use Docker and Ansible to deploy this application, as described in the [d4s2-webapp](https://github.com/Duke-GCB/gcb-ansible-roles/tree/master/d4s2_webapp) role.

Docker images are built on-demand as described by the [datadelivery.yml](https://github.com/Duke-GCB/gcb-ansible/blob/master/datadelivery.yml) playbook
