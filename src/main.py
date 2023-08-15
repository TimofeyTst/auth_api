import sentry_sdk
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.schemas import UserCreate, UserRead, UserUpdate
from src.auth.users import auth_backend, current_active_user, fastapi_users
from src.config import app_configs, settings
from src.database import User

app = FastAPI(**app_configs)


# @app.on_event("startup")
# async def startup_event():
#     # Initialize Redis
#     pool = aioredis.ConnectionPool.from_url(
#         settings.REDIS_URL, max_connections=10, decode_responses=True
#     )
#     redis.redis_client = aioredis.Redis(connection_pool=pool)

#     # # Initialize SQLAlchemy async session
#     # async with AsyncSession() as session:
#     #     yield session


# @app.on_event("shutdown")
# async def shutdown_event(session: AsyncSession = Depends()):
#     await session.close()
#     await redis.redis_client.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
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
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
