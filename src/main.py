from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status, Depends
from fastapi.encoders import jsonable_encoder

from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.auth.base_config import auth_backend, current_user
from src.auth.base_config import fastapi_users
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.config import REDIS_HOST, REDIS_PORT
from src.operations.router import router as router_operations
from src.tasks.router import router as router_tasks
from src.pages.router import router as router_pages
from src.chat.router import router as router_chat

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

app = FastAPI(title='Trading App')

app.mount("/static", StaticFiles(directory="src/static"), name="static")   # для подключения статического контента


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'detail': exc.errors()})
    )


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_operations)
app.include_router(router_tasks)
app.include_router(router_pages)
app.include_router(router_chat)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS", "DELETE", "PUT", "PATCH", "POST"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)



@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get("/upprotected-route")
def unprotected_route():
    return "Hello, anonym"

# deprecated
# @app.on_event("startup")
# async def startup():
#     redis = aioredis.from_url("redis://localhost")
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
@asynccontextmanager
async def lifespan():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

