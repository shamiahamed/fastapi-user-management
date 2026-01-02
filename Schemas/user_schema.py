from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str
    role_id: int 

    @field_validator("user_name") 
    def name_must_not_be_empty(cls, value: str):
        if not value.strip():
            raise ValueError("User Name must not be empty")
        return value

    @field_validator("password")
    def password_min_length(cls, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        return value

    # ADD THIS TO FIX SWAGGER EXAMPLE
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_name": "",
                "email": "user@example.com",
                "password": "password",
                "role_id": 0
            }
        }
    }

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    role_id: Optional[int] = None 
    is_active: Optional[bool] = None

    @field_validator("user_name") 
    def name_not_empty(cls, value: Optional[str]):
        if value is not None and not value.strip():
            raise ValueError("User Name must not be empty")
        return value

class UserResponse(BaseModel):
    user_id: int                               
    user_name: str
    email: EmailStr
    role_id: int 
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None  

    model_config = {
        "from_attributes": True
    }

class HolidayResponse(BaseModel):
    id: int
    data: str
    message: str
    image: Optional[str] = None
    image_type: Optional[str] = None

    # This is the "Key" that allows Pydantic to read the Database Object
    model_config = ConfigDict(from_attributes=True)