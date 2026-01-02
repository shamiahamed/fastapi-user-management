from fastapi import HTTPException, status

def validate_user(user_id:str, current_user):
    if str(current_user.user_id) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied"
        )