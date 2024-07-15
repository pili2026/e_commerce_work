import os

from fastapi import APIRouter


version_router = APIRouter()


@version_router.get("/version")
async def version():
    safeart_version = os.getenv("SAFEART_VERSION", "dev")
    return {"safeart": safeart_version}
