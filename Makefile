clean:
	rm -fr data

data:
	mkdir data


# Using poetry

install:
	poetry install

test: install
	poetry run pytest

test-watch: install
	poetry run pytest-watch

check: install
	poetry run pylama

style: install
	poetry run isort toubib tests
	poetry run black toubib tests

run-alembic: install data
	sqlalchemy_url='sqlite:///data/db.sqlite?check_same_thread=false' poetry run alembic upgrade head

run-app: run-alembic
	sqlalchemy_url='sqlite:///data/db.sqlite?check_same_thread=false' poetry run hypercorn toubib.main:app --reload


# Using docker

docker-build:
	docker build . -t toubib:latest

docker-test: data docker-build
	docker run -t -i -p 8000:8000 -v `pwd`/data:/data toubib:latest pytest

docker-run-alembic: data docker-build
	docker run -t -i -v `pwd`/data:/data toubib:latest alembic upgrade head

docker-run-app: docker-run-alembic
	docker run -t -i -p 8000:8000 -v `pwd`/data:/data toubib:latest
