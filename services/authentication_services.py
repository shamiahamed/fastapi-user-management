from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from Schemas.models.structure import User
from Schemas.authentic_schema import LoginRequest
from core.exception import ValidationException
from core.hash_password import verify_password
from dependencies.authentication import create_access_token


async def login_user(db: AsyncSession, payload: LoginRequest):
    result = await db.execute(
        select(User).where(
            User.email == payload.email,
            User.is_active.is_(True)
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise ValidationException("Invalid email or password")

    if not verify_password(payload.password, user.password):
        raise ValidationException("Invalid email or password")

    token = create_access_token(
        data={
            "user_id": str(user.user_id),
            "email": user.email,
            "role": user.role_id,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

