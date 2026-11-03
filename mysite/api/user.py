from fastapi import APIRouter, HTTPException, Depends
from mysite.database.models import UserProfile
from mysite.schemas.user_schema import (UserProfileInputSchema,
                                        UserProfileUpdateSchema,
                                        UserProfileOutputSchema)
from mysite.database.db import SessionLocal
from sqlalchemy.orm import Session
import bcrypt
from typing import List


user_router = APIRouter(prefix='/users', tags=['User CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:  # ограничение алгоритма bcrypt
        raise ValueError('Пароль не должен быть длиннее 72 байт')
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode('utf-8')


def check_unique(db: Session, username: str, email: str | None, user_id: int | None = None):
    """Username жана email башка колдонуучуда жок экенин текшерет."""
    query = db.query(UserProfile).filter(UserProfile.username == username)
    if user_id is not None:
        query = query.filter(UserProfile.id != user_id)
    if query.first():
        raise HTTPException(detail='Мындай username бар экен', status_code=400)

    if email:
        query = db.query(UserProfile).filter(UserProfile.email == email)
        if user_id is not None:
            query = query.filter(UserProfile.id != user_id)
        if query.first():
            raise HTTPException(detail='Мындай email бар экен', status_code=400)


@user_router.post(path='/', response_model=UserProfileOutputSchema)
async def user_create(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    check_unique(db, user.username, user.email)

    user_data = user.model_dump()
    try:
        user_data['password'] = get_password_hash(user_data['password'])
    except ValueError:
        raise HTTPException(detail='Пароль өтө узун (максимум 72 байт)', status_code=400)

    user_db = UserProfile(**user_data)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get(path='/', response_model=List[UserProfileOutputSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.get(path='/{user_id}/', response_model=UserProfileOutputSchema)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай колдонуучу жок', status_code=400)

    return user_db


@user_router.put(path='/{user_id}/', response_model=dict)
async def user_update(user_id: int, user: UserProfileUpdateSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай колдонуучу жок', status_code=400)

    check_unique(db, user.username, user.email, user_id=user_id)

    user_data = user.model_dump()
    password = user_data.pop('password')
    if password:
        try:
            user_data['password'] = get_password_hash(password)
        except ValueError:
            raise HTTPException(detail='Пароль өтө узун (максимум 72 байт)', status_code=400)

    for user_key, user_value in user_data.items():
        setattr(user_db, user_key, user_value)

    db.commit()
    db.refresh(user_db)
    return {"message": "Колдонуучунун маалыматтары өзгөрүлдү"}


@user_router.delete(path='/{user_id}/', response_model=dict)
async def user_delete(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='Мындай колдонуучу жок', status_code=400)

    db.delete(user_db)
    db.commit()
    return {"message": "Колдонуучу өчүрүлдү"}
