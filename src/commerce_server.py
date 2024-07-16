import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from graphql_api.schema_registry import graphql_router
from restful_api.handler.health import health_check_router
from restful_api.handler.order import order_router
from restful_api.handler.order_detail import order_detail_router
from restful_api.handler.product import product_router
from restful_api.handler.authentication import authentication_router
from restful_api.version import version_router
from util.config_manager import ConfigManager, set_config_manager
from util.db_manager import get_db_manager
from util.logging_configurer import configure_logging
from util.route_prefix import RoutePrefix


log = logging.getLogger(__name__)


class CommerceServer:
    def __init__(self, config_path: str):
        config_manager = ConfigManager(config_path)
        set_config_manager(config_manager)

        config = config_manager.get_config()
        configure_logging(config["LOG_LEVEL"])
        readable_config = config_manager.get_readable_config()

        log.info("Commerce Configuration Path: %s", config_path)
        log.info("Commerce Configuration: %s", readable_config)

        self.config = config
        self.app = FastAPI(lifespan=self.__lifespan)
        self.__setup_router()
        self.__setup_middleware()

    def start(self):
        uvicorn.run(self.app, host="0.0.0.0", port=8000)

    def __setup_router(self):
        # NOTE: For internal services usage without /api prefix
        self.app.include_router(health_check_router)

        self.app.include_router(version_router, prefix=RoutePrefix.API)
        self.app.include_router(order_router, prefix=RoutePrefix.API, tags=["order"])
        self.app.include_router(order_detail_router, prefix=RoutePrefix.API, tags=["order_detail"])
        self.app.include_router(product_router, prefix=RoutePrefix.API, tags=["product"])
        self.app.include_router(authentication_router, prefix=RoutePrefix.API, tags=["authentication"])

        self.app.include_router(graphql_router, prefix=RoutePrefix.GRAPHQL, tags=["graphql"])

    def __setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
        )

    @asynccontextmanager
    async def __lifespan(self, app: FastAPI):
        await self.__on_startup()
        yield
        await self.__on_shutdown()

    async def __on_startup(self):
        db_manager = get_db_manager()
        log.info("The async db connection string of the Web Server is: %s", db_manager.async_db_connection_string)

        await db_manager.wait_for_db_available()

    async def __on_shutdown(self):
        log.info("Shutting down the Web Server.")

        db_manager = get_db_manager()
        await db_manager.close_engine()

        log.info("Successfully shut down the Web Server.")
