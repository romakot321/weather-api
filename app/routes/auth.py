from contextlib import asynccontextmanager

from fastapi import Depends, APIRouter, Response

from app.db.tables import User
from app.schemas.auth import AuthUserCreateSchema, AuthUserReadSchema, AuthUserUpdateSchema
from app.services.auth import (
    SECRET,
    auth_backend,
    fastapi_users,
)
from app.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)
router.include_router(
    fastapi_users.get_register_router(AuthUserReadSchema, AuthUserCreateSchema),
)

