import logging
import logging.config
import os

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base

config = context.config

if config.config_file_name:
    logging.config.fileConfig(config.config_file_name)
else:
    logging.basicConfig(level=logging.DEBUG)

target_metadata = declarative_base().metadata

if config.get_main_option("sqlalchemy.url") is None:
    config.set_main_option("sqlalchemy.url", os.environ["sqlalchemy_url"])


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
