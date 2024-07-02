import bcrypt

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from sqlalchemy.future import select

from question_5.db.models.user import User as UserModel
from question_5.db.models.country import Country as CountryModel
from question_5.db.schema import User


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()

async def create_user(db: AsyncSession, user: User):
    """
    Creates user in the database.
    """
    # hash password, store salt
    name = user.name
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(user.password.encode('utf-8'), salt)

    db_user = UserModel(name, password, salt)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

async def authenticate_user(db: AsyncSession, user: User) -> bool:
    """
    Authenticates user into the system.
    """
    db_user: UserModel = await get_user_by_name(db, name=user.name)
    if db_user is None:
        return False
    else:
        db_user = db_user[0]
        return bcrypt.checkpw(user.password.encode('utf-8'), db_user.password)

async def get_user_by_name(db: AsyncSession, name: str):
    """
    Retrieves user by username.
    """
    query = select(UserModel).filter(UserModel.name == name)
    result = await db.execute(query)
    user = result.first()

    return user

async def check_country_code(db: AsyncSession, country_code: str) -> bool:
    """
    Checks if provided country code exists.
    """
    query = select(CountryModel).filter(CountryModel.code == country_code.upper())
    result = await db.execute(query)
    country = result.fetchone()
    
    if country is None:
        return False
    else:
        return True