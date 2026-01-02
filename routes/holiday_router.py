from fastapi import Depends, UploadFile, Form, File, APIRouter
from typing import Optional
from decorators.response_handler import handle_api_response
from decorators.api_logger import api_logger
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from controllers.holiday_controller import HolidayController

router = APIRouter(prefix="/holidays", tags=["Holiday"])

@router.post("/")
@api_logger
@handle_api_response("Holiday Announcement created successfully")
async def create_holiday(
    data: str = Form(...), 
    message: str = Form(...), 
    image_file: Optional[UploadFile] = File(None), 
    image_base64: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    # The 'result' is the dictionary from the controller
    # The decorator wraps it into: {"status": True, "message": "...", "data": result}
    result = await HolidayController.create_announcement(db, data, message, image_file, image_base64)
    return result