# Datastore
A platform that allows the user to store multiple types of forms and responses.
The user can integrate 3rd party platform with the form response.

## DB design
![Alt text](./db_design.png?raw=true )

## Platform design
![Alt text](./platform_design.png?raw=true )

## Tech stack
- Python
- Django framework
- Postgres
- Django rest framework
- Celery 
- Redis (Celery broker)

## Local development setup 

1. Clone the repo to local
    ```
    git clone https://github.com/rishikant42/Atlan-DataStore.git
    ```

### Setup without docker

1. DB setup
    - Please make sure you have postgres server(version 11 or higher) installed and running
    - Create the postgres database and set it as default
    - Update the db configurations in datastore/settings.py or local_settings.py

2. Redis setup
    - Please make sure you have redis-server running in local, If not please install the redis and start the server.
        ```
        $ redis-cli ping
        PONG
        ```

3. Add and update project local settings if needed
    ```
    cp datastore/datastore/local_settings.py.local datastore/datastore/local_settings.py
    ```

4. Create virtual environment and install app dependencies
    - please set the correct python version for this project as specified in `.python-version`, and create a virtual environment as shown below:
        ```
        python -m venv venv
        source venv/bin/activate
        ```
    - Install application dependencies
        ```
        pip install -r requirements.txt
        ```

5. Start Django server
    - Run Django migrations
        ```
        python manage.py migrate
        ```
    - Run Django server
        ```
        python manage.py runserver 8000
        ```

6. Run celery worker
    ```
    celery -A datastore worker -l info
    ```

### Setup with docker-compose
1. Start project services

    ```
    docker-compose up --build
    ```

### TODO
- Add unit test cases
- Add API validations
- The manual testing of Google sheet action. As of now, I have only tested the core logic of the platform. The google sheet integration-specific code is written on top of the core logic but this is not yet tested.


### APIs demo

1. Create form API
```
Request:
curl --location --request POST 'http://127.0.0.1:8787/api/store/forms/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "form1",
    "user_uid": "35d57f6a-9b62-4b3a-9421-8130da33b5fd"
}'

Response:
{
    "uid": "bb0d1c7a-5f1f-434b-b3fd-2c0cf58f2d1f",
    "name": "form1",
    "questions": [],
    "responses": []
}
```

2. Create question API
```
Request:
curl --location --request POST 'http://127.0.0.1:8787/api/store/questions/' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
    "title": "title1",
    "form_uid": "bb0d1c7a-5f1f-434b-b3fd-2c0cf58f2d1f",
    "keyword": "keyword1",
    "options": [
        {"label": "l1", "code": "c1"},
        {"label": "l2", "code": "c2"}
    ]
}
]'
Response:
[
    {
        "uid": "9621a03d-0ccb-41b1-ba64-0ad4f9b692ee",
        "question_type": "SINGLE_CHOICE",
        "title": "title1",
        "description": null,
        "keyword": "keyword1",
        "is_mandatory": true,
        "allow_none_option": false,
        "allow_all_option": false,
        "lower_limit": null,
        "upper_limit": null,
        "allow_decimal": false,
        "date_format": null,
        "time_format": null,
        "question_options": [
            {
                "uid": "5f5c14bb-9138-4535-b6f2-ca940ecf6e82",
                "label": "l1",
                "code": "c1"
            },
            {
                "uid": "ca72452c-c37f-4008-a7a8-3865fb9aa59a",
                "label": "l2",
                "code": "c2"
            }
        ]
    }
]
```

3. Create response API
```
Request:
curl --location --request POST 'http://127.0.0.1:8787/api/store/responses/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_uid": "35d57f6a-9b62-4b3a-9421-8130da33b5fd",
    "form_uid": "bb0d1c7a-5f1f-434b-b3fd-2c0cf58f2d1f",
    "answers": [
        {
            "question_uid": "9621a03d-0ccb-41b1-ba64-0ad4f9b692ee",
            "value": "code1"
        }
    ]
}'
Reponse:
{
    "uid": "325b93d2-bad1-46f6-8a68-9258d5ade5ab",
    "answers": [
        {
            "question_uid": "9621a03d-0ccb-41b1-ba64-0ad4f9b692ee",
            "value": "code1"
        }
    ]
}
```

**NOTE:** The create response API triggers an action task attached to the form. This is done asynchronously.

4. Get form questions and responses
```
Request:
curl --location --request GET 'http://127.0.0.1:8787/api/store/forms/bb0d1c7a-5f1f-434b-b3fd-2c0cf58f2d1f/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "form1",
    "user_uid": "35d57f6a-9b62-4b3a-9421-8130da33b5fd"
}'
Response:
{
    "uid": "bb0d1c7a-5f1f-434b-b3fd-2c0cf58f2d1f",
    "name": "form1",
    "questions": [
        {
            "uid": "9621a03d-0ccb-41b1-ba64-0ad4f9b692ee",
            "question_type": "SINGLE_CHOICE",
            "title": "title1",
            "description": null,
            "keyword": "keyword1",
            "is_mandatory": true,
            "allow_none_option": false,
            "allow_all_option": false,
            "lower_limit": null,
            "upper_limit": null,
            "allow_decimal": false,
            "date_format": null,
            "time_format": null,
            "question_options": [
                {
                    "uid": "5f5c14bb-9138-4535-b6f2-ca940ecf6e82",
                    "label": "l1",
                    "code": "c1"
                },
                {
                    "uid": "ca72452c-c37f-4008-a7a8-3865fb9aa59a",
                    "label": "l2",
                    "code": "c2"
                }
            ]
        }
    ],
    "responses": [
        {
            "uid": "325b93d2-bad1-46f6-8a68-9258d5ade5ab",
            "answers": [
                {
                    "value": "code1",
                    "question_uid": "9621a03d-0ccb-41b1-ba64-0ad4f9b692ee"
                }
            ]
        }
    ]
}
```
