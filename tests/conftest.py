import os

import httpx
from alembic import command
from alembic.config import Config
from asgi_lifespan import LifespanManager
from faker import Faker
from pytest import fixture


@fixture(scope="session")
def faker():
    return Faker()


@fixture(scope="session")
def db_url():
    # https://stackoverflow.com/a/48234567
    return "sqlite:///tests/testdb.sqlite?check_same_thread=false"


@fixture
def sqla_modules():
    from toubib import sqla  # noqa


@fixture
async def app():
    from toubib.main import app

    async with LifespanManager(app):
        yield app


@fixture
async def client(app):
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://app"
        ) as client:
            yield client


@fixture(scope="session", autouse=True)
def db_migration(db_url, sqla_connection, alembic_ini_path):
    """Run alembic upgrade at test session setup and downgrade at tear down.

    Override fixture `alembic_ini_path` to change path of `alembic.ini` file.
    """
    alembic_config = Config(file_=alembic_ini_path)
    alembic_config.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(alembic_config, "head")
    yield
    command.downgrade(alembic_config, "base")
    os.unlink("./tests/testdb.sqlite")
