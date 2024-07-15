import argparse
import asyncio
import logging

from seed.system_data_generator import get_app_default_data_generator
from util.config_manager import ConfigManager, set_config_manager
from util.db_manager import get_db_manager
from util.db_migration_manager import get_db_migration_manager
from util.logging_configurer import configure_logging

log = logging.getLogger(__name__)


async def main():
    parser = argparse.ArgumentParser(description="args to start up the web application.")
    parser.add_argument("--config_path", help="The config path of the db_migration_runner.py", required=True)
    args = parser.parse_args()

    config_path = args.config_path if args.config_path else "/etc/app_config.yml"
    config_manager = ConfigManager(config_path)
    set_config_manager(config_manager)

    config = config_manager.get_config()
    configure_logging(config["LOG_LEVEL"])
    readable_config = config_manager.get_readable_config()

    log.info("DB Migration Configuration Path: %s", config_path)
    log.info("DB Migration Configuration: %s", readable_config)

    db_manager = get_db_manager()
    await db_manager.wait_for_db_available()

    db_migration_manager = get_db_migration_manager()
    db_migration_manager.run_db_migration()

    system_data_generator = get_app_default_data_generator()
    await system_data_generator.generate_app_default_data()


if __name__ == "__main__":
    asyncio.run(main())
