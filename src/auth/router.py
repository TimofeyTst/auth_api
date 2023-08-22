from fastapi import APIRouter

from src.auth.schemas import UserCreate, UserRead
from src.auth.users import auth_backend, auth_config, fastapi_users, google_oauth_client

router = APIRouter()

router.include_router(fastapi_users.get_auth_router(auth_backend))

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

router.include_router(
    fastapi_users.get_reset_password_router(),
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        auth_config.JWT_SECRET,
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix="/google",
)
