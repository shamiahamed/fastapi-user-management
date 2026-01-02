# auth_controller.py
from services.authentication_services import login_user

class AuthController:
    @staticmethod
    async def login_logic(db, payload):
        # Service returns the raw token dictionary: {"access_token": "...", "token_type": "bearer"}
        token_data = await login_user(db, payload)
        
        # JUST return the raw data, do not format it here
        return token_data