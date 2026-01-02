from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from Schemas.authentic_schema import LoginRequest
from controllers.authentication_controller import AuthController 
from decorators.api_logger import api_logger

from core.common import format_response

router = APIRouter(prefix="/authentication", tags=["Authentication"], responses={200: {"content": None}, 422: {"content": None}})

@router.post("/login")
@api_logger
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    # Get the token and user data from your controller
    auth_result = await AuthController.login_logic(db, payload)
    
    # We wrap the result here. 
    # we pass it directly to data.
    return format_response(
        status=200, 
        data=auth_result, 
        message="Login successful"
    )