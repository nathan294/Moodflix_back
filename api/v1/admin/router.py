from fastapi import APIRouter, Depends
from firebase_admin import auth
from sqlalchemy.orm import Session

from api.v1.admin.firebase import delete_firebase_user, exchange_custom_token_for_id_token
from api.v1.commons.dependencies import get_db
from api.v1.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.get("/get_custom_token")
def get_custom_token(user_id: str = "lsQvnap97eS77zaMBGrT3VfkGfq1"):
    """Generate a JWT Token used for other API Endpoints.

    Firebase user IDs : \n
    Dev :
    * lsQvnap97eS77zaMBGrT3VfkGfq1

    Stage :
    * EvX8Oou45UXR5j5M1AaxGrlnnHy2
    """
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
