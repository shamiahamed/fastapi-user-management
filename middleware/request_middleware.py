import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.config import settings

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        start_time = time.time()  #time.time() comes in timestamp with floating point seconds

        response = await call_next(request)

        process_time = round(time.time() - start_time, 4)  #round to 4 decimal digit

        logger.info(
            "Request completed",
            extra={
                "method": request.method,  
                "path": request.url.path,
                "status_code": response.status_code,
                "duration": process_time,
            },
        )

        return response
