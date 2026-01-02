from sqlalchemy.ext.asyncio import AsyncSession
from services.holiday_services import create_holiday_service

class HolidayController:
    @staticmethod
    async def create_announcement(db: AsyncSession, data: str, message: str, file, base64_file):
        # We pass both file objects to the service
        new_holiday = await create_holiday_service(db, data, message, file, base64_file)

        if not new_holiday:
            return None
        
        # Returns the dictionary for the decorator
        return {
            "id": new_holiday.id,
            "data": new_holiday.data,
            "message": new_holiday.message,
            "image": new_holiday.image,
            "image_type": new_holiday.image_type
        }