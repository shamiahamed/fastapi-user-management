from fastapi import HTTPException, status

class AppException(HTTPException):
    def __init__(self, message: str, status_code: int):
        # We manually build the dict here to match format_response
        # status is set to False because these are all error classes
        super().__init__(
            status_code=status_code,
            detail={
                "status": False,  
                "data": None,
                "message": message
            },
        )

class ValidationException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

class DatabaseException(AppException):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )