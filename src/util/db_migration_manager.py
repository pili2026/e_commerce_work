import argparse
import logging

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory

from util.app_error import AppError, ErrorCode
from util.config_manager import ConfigManager, get_config_manager
from util.db_manager import DBManager, get_db_manager


log = logging.getLogger(__name__)

__DB_MIGRATION_MANAGER = None


ALEMBIC_UPGRADE_KEYWORD = ["head", "+1"]
ALEMBIC_DOWNGRADE_KEYWORD = ["base", "-1"]


class DBMigrationManager:
    def __init__(self, config_manager: ConfigManager, db_manager: DBManager):
        app_config = config_manager.get_config()
        config_path_arg = f"config_path={config_manager.config_path}"

        self.cmd_opts = argparse.Namespace()
        self.cmd_opts.x = [config_path_arg]
        self.alembic_config = Config("alembic.ini", cmd_opts=self.cmd_opts)
        self.db_migration_head_version = app_config["DB_MIGRATION_REVISION"]
        self.config_manager = config_manager
        self.db_manager = db_manager

    def run_db_migration(self):
        log.info("Ready to run DB Migration")

        target_revision = self._get_target_revision()
        log.info("Target Revision: %s", target_revision)

        current_revision = self._get_current_revision()
        log.info("Current Revision: %s", current_revision)

        if current_revision is None:
            log.info("There are no versions available yet.")
            command.upgrade(self.alembic_config, target_revision)
            return

        history_revision_list = self._get_history_revision_list()
        log.info("History Revision List: %s", history_revision_list)

        self._update_database(target_revision, current_revision, history_revision_list)

    def _update_database(self, target_revision, current_revision, history_revision_list):
        if target_revision in ALEMBIC_UPGRADE_KEYWORD or self._is_target_a_newer_version(
            target_revision, current_revision, history_revision_list
        ):
            command.upgrade(self.alembic_config, target_revision)
        elif target_revision in ALEMBIC_DOWNGRADE_KEYWORD or self._is_target_an_older_version(
            target_revision, current_revision, history_revision_list
        ):
            command.downgrade(self.alembic_config, target_revision)
        else:
            log.info("No upgrade or downgrade needed.")

    def _is_target_a_newer_version(self, target_revision, current_revision, history_revision_list) -> bool:
        if target_revision in ALEMBIC_UPGRADE_KEYWORD or target_revision in ALEMBIC_DOWNGRADE_KEYWORD:
            return False

        # The smaller the index, the newer the version.
        return history_revision_list.index(target_revision) < history_revision_list.index(current_revision)

    def _is_target_an_older_version(self, target_revision, current_revision, history_revision_list) -> bool:
        if target_revision in ALEMBIC_UPGRADE_KEYWORD or target_revision in ALEMBIC_DOWNGRADE_KEYWORD:
            return False

        # The larger the index, the older the version.
        return history_revision_list.index(target_revision) > history_revision_list.index(current_revision)

    def _get_target_revision(self) -> str:
        app_config = self.config_manager.get_config()
        target_revision = app_config["DB_MIGRATION_REVISION"]
        return target_revision

    def _get_history_revision_list(self) -> list[str]:
        script = ScriptDirectory.from_config(self.alembic_config)
        historical_revision_list = [rev.revision for rev in script.walk_revisions()]
        return historical_revision_list

    def _get_current_revision(self) -> str:
        engine = self.db_manager.get_sync_engine()
        with engine.connect() as connection:
            context = MigrationContext.configure(connection)
            return context.get_current_revision()


def get_db_migration_manager() -> DBMigrationManager:
    global __DB_MIGRATION_MANAGER

    if __DB_MIGRATION_MANAGER is not None:
        return __DB_MIGRATION_MANAGER

    if get_config_manager() is None:
        raise AppError(
            message="Can not initialize the DBMigrationManager, ConfigManager has not been initialized yet.",
            code=ErrorCode.SERVER_ERROR,
        )

    __DB_MIGRATION_MANAGER = DBMigrationManager(
        config_manager=get_config_manager(),
        db_manager=get_db_manager(),
    )
    return __DB_MIGRATION_MANAGER
