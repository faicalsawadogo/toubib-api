# [Toubib](https://en.wiktionary.org/wiki/toubib) API - Code Challenge

You are given a skeleton of an Electronic Medical Record API that returns json documents.

The app is a [FastAPI](https://fastapi.tiangolo.com/) app running against an sqlite DB.

You have to implement 3 functionalities:

1. Create patient record;
2. Get a patient record;
3. List patient records alphabetically by last name and by pages of 10 records at a time;

## 1. Create patient record

`POST /v1/patients` with request body (all fields are required, email is unique per
patient):

```json
{
    "email": "tracy@edwards.com",
    "first_name": "Tracy",
    "last_name": "Edwards",
    "date_of_birth": "1962-09-05",
    "sex_at_birth": "FEMALE"
}

```

Returns:

```json
{
    "data": {
        "id": 1,
        "email": "tracy@edwards.com",
        "first_name": "Tracy",
        "last_name": "Edwards",
        "date_of_birth": "1962-09-05",
        "sex_at_birth": "FEMALE"
    }
}
```

## 2. Getting a patient record

`GET /v1/patients/1` returns:

```json
{
    "data": {
        "id": 1,
        "email": "tracy@edwards.com",
        "first_name": "Tracy",
        "last_name": "Edwards",
        "date_of_birth": "1962-09-05",
        "sex_at_birth": "FEMALE"
    }
}
```

## 3. List patient records alphabetically by last name and by pages of 10 records at a time

`GET /v1/patients?offset=40&limit=10` returns:

```json
{
    "data": [
        {
            "id": 17,
            "email": "mulatu@astatke",
            "first_name": "Mulatu",
            "last_name": "Astatke",
            "date_of_birth": "1943-12-19",
            "sex_at_birth": "MALE"
        },
        {
            "id": 21,
            "email": "tracy@edwards.com",
            "first_name": "Tracy",
            "last_name": "Edwards",
            "date_of_birth": "1962-09-05",
            "sex_at_birth": "FEMALE"
        }
    ],
    "meta": {
        "offset": 40,
        "total_items": 42,
        "total_pages": 5,
        "page_number": 5
    }
}
```

## Quickstart


You'll need python 3.10 and [poetry](https://python-poetry.org/).
OR, you can use docker. A `Makefile` with all usefull commands is provided.

### Install project

```sh
poetry install
```

### Run tests
```sh
make test
```

### Other commands available:

```sh
make test-watch  # run test in live reload
make check       # linting
make style       # code formatter
...              # many more
```



### DB Migrations

Migrations are managed with [Alembic](https://alembic.sqlalchemy.org/). Migrations
scripts are located in `toubib/db/versions`.

- To list migrations history:

  ```sh
  poetry run alembic history
  ```

- To upgrade to head:

  ```sh
  poetry run alembic upgrade head
  ```

- To downgrade to base:

  ```sh
  poetry run alembic downgrade base
  ```

## Evaluation

Your submission will be evaluated according to three categories:

1. **Developer Experience and Code Quality.**
2. **Functionality.** Does this application implement the spec and run?
3. **Tests and Testability.** Is the design testable? Is the core functionality tested?
