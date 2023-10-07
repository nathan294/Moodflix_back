from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import api.models as mdl
import api.user.schemas as sch
from api.commons.dependencies import get_db

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get("/{user_id}", response_model=sch.User)
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
    Update a user email based on his user_id
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


@router.delete("/{user_id}", response_model=bool)
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a user based on his user_id
    """
    # Old sqlalchemy syntaxe, to be modified
    db.query(mdl.User).filter_by(id=user_id).delete()
    db.commit()
    return True
