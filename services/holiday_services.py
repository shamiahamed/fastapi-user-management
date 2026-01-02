import os
import shutil
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from Schemas.models.structure import HolidayAnnouncement

# 1. Physical storage path
UPLOAD_DIR = "static/uploads/holidays"

async def create_holiday_service(db: AsyncSession, data: str, message: str, file=None, base64_file=None):
    final_image_data = ""
    selected_type = None

    # PHYSICAL FILE UPLOAD ---
    # We save the actual file to the server disk using shutil.
    if file and file.filename != "":
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Save the file locally
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        final_image_data = file_path  # We store the PATH string
        selected_type = "folder"

    # BASE64 CONVERSION ---
    # store that massive string directly in the database column.
    elif base64_file and base64_file.filename != "":
        # 1. Read the binary data from the uploaded file
        image_bytes = await base64_file.read()
        
        # 2. Encode to base64 text
        encoded_string = base64.b64encode(image_bytes).decode("utf-8")
        
        # 3. Format as a Data URI (browser ready)
        mime_type = base64_file.content_type or "image/png"
        final_image_data = f"data:{mime_type};base64,{encoded_string}"
        
        selected_type = "base64"

    # NO IMAGE ---
    else:
        final_image_data = None
        selected_type = None

    # Save the result (either a File Path or a Base64 String) to MySQL
    new_holiday = HolidayAnnouncement(
        data=data,
        message=message,
        image=final_image_data,
        image_type=selected_type
    )
    
    db.add(new_holiday)
    await db.commit()
    await db.refresh(new_holiday)
    return new_holiday