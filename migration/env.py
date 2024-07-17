import logging
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from repository.model.base import Base
from util.config_manager import get_config_manager, set_config_manager, ConfigManager
from util.db_manager import get_db_manager
from util.logging_configurer import configure_logging

log = logging.getLogger(__name__)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
x_argu = context.get_x_argument(as_dictionary=True)

config_path = x_argu.get("config_path")
if not config_path:
    raise ValueError("Config path must be provided")

# Initialize ConfigManager manually
config_manager = ConfigManager(config_path)
set_config_manager(config_manager)

app_config = config_manager.get_config()
configure_logging(app_config["LOG_LEVEL"])
readable_app_config = config_manager.get_readable_config()

log.info("Alembic Command Configuration Path: %s", config_path)
log.info("Alembic Command Configuration: %s", readable_app_config)

db_manager = get_db_manager()
log.info("The sync db connection string of the Alembic Command Line is: %s", db_manager.sync_db_connection_string)

config.set_main_option("sqlalchemy.url", db_manager.sync_db_connection_string)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
