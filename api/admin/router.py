from fastapi import APIRouter, Depends
from firebase_admin import auth
from sqlalchemy.orm import Session

from api.admin.firebase import delete_firebase_user, exchange_custom_token_for_id_token
from api.commons.dependencies import get_db
from api.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/get_custom_token")
def get_custom_token(user_id: str = "aeANvF2kQoQVUT3GK7biyV1MtFf2"):
    custom_token = auth.create_custom_token(user_id)
    token = exchange_custom_token_for_id_token(custom_token.decode())
    return token


@router.delete("/users/")
async def delete_all_users(db: Session = Depends(get_db)):
    # Fetch the user
    users = db.query(User).all()

    if not users:
        return {"error": "No user"}

    for user in users:
        # Delete from Firebase
        delete_firebase_user(user.firebase_id)

        # Delete from PostgreSQL
        db.delete(user)
    db.commit()
    return {"message": "User table emptied"}
