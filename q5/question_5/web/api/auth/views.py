
from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from question_5.db.dependencies import get_db_session, create_user, authenticate_user, get_user_by_name, check_country_code
from question_5.db.schema import User

router = APIRouter()


@router.post("/auth", status_code=status.HTTP_200_OK)
async def auth(user: User, db: AsyncSession = Depends(get_db_session)):
    """
    Logs a user in.
    """
    # check country code
    country_code = user.name[:2]
    user.name = user.name[2:]

    country_exists = await check_country_code(db=db, country_code=country_code)

    if country_exists:
        auth_status = await authenticate_user(db=db, user=user)
        if not auth_status:
            raise HTTPException(status_code=401, detail="Invalid username/password.")
        else:
            return True
    else:
        raise HTTPException(status_code=403, detail="Invalid country code provided.")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User, db: AsyncSession = Depends(get_db_session)):
    """
    Creates a user in the database.
    """
    # check if username already exists
    db_user = await get_user_by_name(db, name=user.name)
    if db_user is not None:
        raise HTTPException(status_code=400, detail="Username already registered.")
    
    return await create_user(db=db, user=user)
