from sqlalchemy.ext.asyncio import AsyncSession
from Schemas.user_schema import UserCreate, UserUpdate
from services.user_services import list_users, get_user, update_user, delete_user, create_user

class UserController:
    @staticmethod
    async def create_user(db: AsyncSession, payload: UserCreate):
        return await create_user(db, payload)

    @staticmethod
    async def get_user(db: AsyncSession, user_id: str):
        return await get_user(db, user_id)

    @staticmethod
    async def update_user(db: AsyncSession, user_id: str, payload: UserUpdate):
        return await update_user(db, user_id, payload)

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: str):
        return await delete_user(db, user_id)
    
    @staticmethod
    async def get_all_users(db: AsyncSession):
        return await list_users(db)