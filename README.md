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
>
```

## Installation (docker)

TBD

## Running the project

### Apply migrations to have latest DB setup
```sh
# run migrations
> python manage.py makemigrations
> python manage.py migrate

# run server (admin interface should be available going to http://localhost:8000/admin)
> python manage.py runserver
```