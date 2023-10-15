from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import api.models as mdl
import api.user.schemas as sch
from api.admin.firebase import delete_firebase_user
from api.commons.dependencies import get_db, verify_firebase_token
from api.models.user import User

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/id/{user_id}", response_model=sch.User)
async def read_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Get a user based on his user_id
    """
    stmt = select(mdl.User).filter_by(id=f"{user_id}")
    db_user = db.scalar(stmt)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return sch.User.model_validate(db_user)


@router.post("/", response_model=sch.User)
async def create_user(user: sch.UserCreate, db: Session = Depends(get_db)):
    """
    Create a user with email and firebase_id
    """
    stmt = select(mdl.User).filter_by(email=f"{user.email}")
    db_user = db.scalar(stmt)
    if db_user:
        raise HTTPException(status_code=409, detail="User already registered")
    db_user = mdl.User(email=user.email, firebase_id=user.firebase_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return sch.User.model_validate(db_user)


@router.put("/", response_model=sch.User)
async def update_user_email(user: sch.UserUpdate, db: Session = Depends(get_db)):
    """
    [DEPRECATED]
    [To be replaced with the possibility to update user's password based on firebase ID]
    """
    stmt = select(mdl.User).filter_by(user_id=user.user_id)
    db_user = db.scalar(stmt)
    if db_user is None:
        return HTTPException(404, "User not found")
    if user.email is None:
        return sch.User.model_validate(db_user)
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return sch.User.model_validate(db_user)


@router.delete("/id/{firebase_id}")
async def delete_user_using_firebase_id(firebase_id: str, db: Session = Depends(get_db)):
    """
    Delete a user based on his firebase_id
    """
    # Fetch the user
    user = db.query(User).filter(User.firebase_id == firebase_id).first()

    if not user:
        return {"error": "User not found"}

    # Delete from Firebase
    delete_firebase_user(user.firebase_id)

    # Delete from PostgreSQL
    db.delete(user)
    db.commit()

    return {"message": "User deleted"}


@router.get("/me")
async def current_user(uid: str = Depends(verify_firebase_token), db: Session = Depends(get_db)):
    db_user = db.get(mdl.User, uid)
    print(db_user.email)
    return uid
