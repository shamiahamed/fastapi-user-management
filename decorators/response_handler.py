from functools import wraps
from core.common import format_response
from core.logging import logger

def handle_api_response(message: str):
    def decorator(func):
        @wraps(func) 
        async def wrapper(*args, **kwargs):
            try:
                # Run the actual controller logic
                result = await func(*args, **kwargs)
                
                # Handle 404 if controller returns None
                if result is None:
                    return format_response(status=404, message="Resource not found")
                
                # Return Success Response
                return format_response(status=200, data=result, message=message)
            
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                return format_response(status=400, message=str(e))
        return wrapper
    return decorator