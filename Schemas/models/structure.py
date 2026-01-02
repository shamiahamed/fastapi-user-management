from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Text
import enum
from database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    role_id = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True)
    
    # Use datetime.now(timezone.utc) for both to avoid the strikethrough/deprecation
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))


class ImageType(enum.Enum):
    base64 = "base64"
    folder = "folder"

class HolidayAnnouncement(Base):
    __tablename__ = "holiday_announcements"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Text, nullable=False)
    message = Column(String(255))
    image = Column(Text) 
    # Use the Enum here
    image_type = Column(Enum(ImageType), nullable=False)

    