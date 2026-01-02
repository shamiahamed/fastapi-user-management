import time
from functools import wraps
from fastapi import Request
from core.logging import logger

def api_logger(func):
   
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        start_time = time.time()          #time.time() comes in timestamp with floating point seconds

        try:
            response = await func(*args, **kwargs)
            #round to 4 decimal digit
            duration = round(time.time() - start_time, 4)  

            path = request.url.path if request else "Unknown Path"
            method = request.method if request else "Unknown Method"
            
            logger.info(
                f"{method} {path} - Duration: {duration}s"
            )

            return response

        except Exception as error:
            logger.error(f"Unhandled API exception: {str(error)}")
            raise error

    return async_wrapper