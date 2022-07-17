# Datastore
A platform that allows the user to store multiple types of forms and responses.
The user can integrate 3rd party platform with the form response.

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
