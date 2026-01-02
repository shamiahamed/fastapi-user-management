from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from Schemas.user_schema import UserCreate, UserUpdate, HolidayResponse
from dependencies.authentication import get_current_user
from dependencies.security import validate_user
from decorators.api_logger import api_logger
from decorators.response_handler import handle_api_response
from database import get_db
from controllers.user_controller import UserController
from controllers.holiday_controller import HolidayController

router = APIRouter(
    prefix="/users", 
    tags=["Users"], 
    responses={
        200: {"description": "Success"}, 
        422: {"description": "Validation Error"}
    }
)

@router.post("/")
@api_logger
@handle_api_response("User created successfully")
async def create_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserController.create_user(db, payload)


#depends only talks with database using asynchronous way to get the current user data
@router.get("/{user_id}")
@api_logger
@handle_api_response("User fetched successfully")
async def get_user_by_id(user_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    validate_user(user_id, current_user)
    # Pass only 2 arguments
    return await UserController.get_user(db, user_id)


@router.put("/{user_id}")
@api_logger
@handle_api_response("User updated successfully")
async def update_user(user_id: str, payload: UserUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    validate_user(user_id, current_user)
    # Pass only 3 arguments
    return await UserController.update_user(db, user_id, payload)


@router.delete("/{user_id}")
@api_logger
@handle_api_response("User deleted successfully")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    validate_user(user_id, current_user)
    # Pass only 2 arguments
    result = await UserController.delete_user(db, user_id)
    return {"user_id": user_id} if result else None


@router.get("/")
@api_logger
@handle_api_response("Users fetched successfully")
async def get_users(db: AsyncSession = Depends(get_db)):
    return await UserController.get_all_users(db)