from uuid import uuid4
from datetime import datetime, timezone

def generate_uuid() -> str:
    return str(uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def format_response(*, status: int = 200, data=None, message: str) -> dict:
    # 1. Simple Success Check
    is_success = 200 <= status < 300

    # 2. Return the data EXACTLY as it is. 
    # Do NOT check for user_id or user_name here.
    return {
        "status": is_success,
        "message": message,
        "data": data  
    }