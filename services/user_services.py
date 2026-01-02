from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from passlib.hash import bcrypt
from Schemas.models.structure import User
from Schemas.user_schema import UserCreate, UserUpdate
from core.exception import ValidationException, DatabaseException

async def create_user(db: AsyncSession, payload: UserCreate):
    try:
        # 1. Hash the password manually
        hashed_pw = bcrypt.hash(payload.password)

        # 2. Explicit Mapping 
        new_user = User(
            user_name=payload.user_name,
            email=payload.email,
            password=hashed_pw,
            role_id=payload.role_id
        )
        
        # 3. Save to database
        db.add(new_user)
        await db.commit()

        return new_user
    except Exception as e:
        await db.rollback()
        raise DatabaseException(f"Create failed: {str(e)}")

async def get_user(db: AsyncSession, user_id: str):
    # Fetch active user by ID
    query = select(User).where(User.user_id == user_id, User.is_active == True)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise ValidationException("User not found")
    return user

class  InsufficientFundsError(Exception):
    pass

def verify_balance(balance, amount):
    print("Checking balance...")
    if amount > balance:
        # 1. RAISE: Execution stops here. The error is "thrown" up.
        raise InsufficientFundsError(f"Error: You need ${amount} but only have ${balance}")
    #return True

async def update_user(db: AsyncSession, user_id: str, payload: UserUpdate):
    user = await get_user(db, user_id)
    try:
        # Update only the fields provided in the request
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        
        user.updated_at = datetime.now(timezone.utc)
        verify_balance(100,500)
        await db.commit()

        return user
    except Exception as e:
        await db.rollback()
        raise DatabaseException(f"Update failed: {str(e)}")
    
    except InsufficientFundsError as e:
        raise 

async def delete_user(db: AsyncSession, user_id: str):
    user = await get_user(db, user_id)
    try:
        user.is_active = False 
        user.updated_at = datetime.now(timezone.utc)
        await db.commit()
        # We return a simple boolean or the object to confirm success
        return True 
    except Exception as e:
        await db.rollback()
        raise DatabaseException(f"Delete failed: {str(e)}")

async def list_users(db: AsyncSession):
    # Return all users where is_active is True
    result = await db.execute(select(User).where(User.is_active == True))
    return result.scalars().all()