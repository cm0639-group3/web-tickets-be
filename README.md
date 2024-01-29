# Flight ticket system (BE)

## Installation (local)

- Clone repository
- Make sure to have python and pip setup in your environment. [Guide](https://packaging.python.org/en/latest/tutorials/installing-packages/).
- Execute the following commands in terminal:

```sh
# create a virtual environment (to better handle the dependencies)
> cd ~/arch-project/
> virtualenv venv

# initiate virtualenv (windows)
> source venv/Scripts/activate
# initiate virtualenv (unix)
> source venv/bin/activate

# install dependencies
> pip install -r requirements.txt
# setup pre-commit hooks (consistent environment)
> pre-commit install

# rename sample env file and assign an environment key
# to run the project
> mv .env.sample .env
```

## Installation (docker)

TBD

## Running the project

### Apply migrations to have latest DB setup
```sh
# run migrations
> python manage.py makemigrations
> python manage.py migrate

# Populate the database (to import countries and cites)
> python manage.py cities_light

# create a superuser
# add base config as shown in .env.sample to configure the superuser
> python manage.py createsuperuser --noinput

# run server (admin interface should be available going to http://localhost:8000/admin)
> python manage.py runserver
```

### Testing API using OpenAPI Spec

1. To visualize the OpenAPI spec go to http://localhost:8000/swagger

![OpenAPI Home](https://github.com/cm0639-group3/web-tickets-be/blob/main/docs/open-api-home.png)

2. Some requests are protected using a JWT authentication token. To generate one,
go to the api endpoint and generate one with the *superuser created previously.*

![Generate a new token](https://github.com/cm0639-group3/web-tickets-be/blob/main/docs/open-api-request-token.png)

3. Go to the top of the page and select the authorize button
![Select top-level authorize](https://github.com/cm0639-group3/web-tickets-be/blob/main/docs/open-api-select-authorize-button.png)

4. Enter the token preceded by a `Bearer` keyword.
![Set token](https://github.com/cm0639-group3/web-tickets-be/blob/main/docs/open-api-set-token.png)


## Docker
1. There is a Dockerfile in the root folder, which is used to build the image and up the container.
   Install Docker if you haven't already.
2. To build an image, you need to run `docker build` in the root of the project.
    - run `docker build -t sa/web.tickets-be:latest .` to create the image
    - run `docker run -p 8000:8000 sa/web.tickets-be:latest` to up the container
