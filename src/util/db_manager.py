import asyncio
import logging
import subprocess
from contextlib import asynccontextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from util.config_manager import ConfigManager, get_config_manager

log = logging.getLogger(__name__)

__DB_MANAGER = None


class DBManager:
    def __init__(self, config_manager: ConfigManager):
        config = config_manager.get_config()
        db_user = config["TIMESCALEDB_DB_USER"]
        db_password = config["TIMESCALEDB_DB_PASSWD"]
        db_host = config["TIMESCALEDB_DB_HOST"]
        db_name = config["TIMESCALEDB_DB_NAME"]

        self.config_manager = config_manager
        self.sync_db_connection_string = self._make_sync_db_connection_string(
            db_user,
            db_password,
            db_host,
            db_name,
        )
        self.async_db_connection_string = self._make_async_db_connection_string(
            db_user,
            db_password,
            db_host,
            db_name,
        )
        self._sync_engine = create_engine(self.sync_db_connection_string, echo=True)
        self._async_engine = create_async_engine(self.async_db_connection_string, echo=True)
        self._session_factory = sessionmaker(bind=self._async_engine, class_=AsyncSession, expire_on_commit=False)

    def _make_sync_db_connection_string(self, db_user, db_password, db_host, db_name: str):
        sync_engine = "postgresql"
        return f"{sync_engine}://{db_user}:{db_password}@{db_host}/{db_name}"

    def _make_async_db_connection_string(self, db_user, db_password, db_host, db_name: str):
        async_engine = "postgresql+asyncpg"
        return f"{async_engine}://{db_user}:{db_password}@{db_host}/{db_name}"

    def get_sync_engine(self):
        return self._sync_engine

    @asynccontextmanager
    async def get_async_session(self):
        async with self._session_factory() as session:
            yield session

    async def close_engine(self):
        log.info("Closing database engine.")
        await self._async_engine.dispose()
        log.info("Successfully closed database engine.")

    async def wait_for_db_available(self):
        log.info("Waiting for DB available, Trying to connect to DB...")

        attempts = 0
        while True:
            try:
                async with self._async_engine.connect():
                    log.info("Database connection successful, DB is available!")
                    break
            except Exception as e:
                attempts += 1
                log.error("Database connection failed. Attempt %s. Retrying in 3 seconds...%s", attempts, e)
                await asyncio.sleep(3)

    def run_upgrade_database_to_head_version(self):
        try:
            subprocess.run(
                ["alembic", "-x", f"config_path={self.config_manager.config_path}", "upgrade", "head"], check=True
            )
            log.info("Alembic upgrade executed successfully.")
        except subprocess.CalledProcessError as e:
            log.error("Alembic upgrade failed: %s", str(e))

    async def truncate_application_tables(self, tables_to_truncate: list[str]):
        log.info("Starting to truncate application tables...")

        async with self._async_engine.begin() as conn:
            for table_name in tables_to_truncate:
                truncate_query = text(f"TRUNCATE TABLE {table_name} CASCADE;")
                await conn.execute(truncate_query)
        log.info("All application tables have been truncated, DB is ready for testing!")


def get_db_manager() -> DBManager:
    global __DB_MANAGER

    if __DB_MANAGER is None:
        config_manager = get_config_manager()
        __DB_MANAGER = DBManager(config_manager)

    return __DB_MANAGER
