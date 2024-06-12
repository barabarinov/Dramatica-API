# Dramatica-API

Welcome to the Dramatica-API! This robust API, built on Django for theatrical management. Whether you're an administrator or an authenticated user, you'll find a comprehensive suite of endpoints to streamline your interaction with the system. From effortlessly browsing and filtering performances to seamlessly managing show sessions and creating reservations, this platform caters to all your theatrical needs.

## Features
* Play Management
* JWT authentication
* Throttling
* Schedule of Performance
* Reservation of Tickets
* Permissions
* Pagination and Filtering
* Media files handling
* Docker Support
* Swagger API Documentation

## Installing using GitHub
If Docker is not being utilized, PostgreSQL must be installed and a database created. Create an `.env` file and define the environment variables using `.env.example`.

```shell
git clone https://github.com/barabarinov/Dramatica-API.git
python -m venv venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
````
## Using Docker
3. Run `docker-compose` command to build and up containers:
```shell
docker-compose up --build
```

![Image Alt text](pic/diagram.png "Database Diagram")
