from fastapi import FastAPI
from .api.main import api_router
from .core.config  import settings

from contextlib import asynccontextmanager
from .core.db import init_db

# this decorator is a context manager that is going to allow us to initialize the database when the app starts,
# clean up resource when the app shuts down and also manage the database connections
@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)
app.include_router(api_router, prefix=settings.API_V1_STR)

