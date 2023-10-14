from fastapi import Header, HTTPException
from firebase_admin import auth

from api.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_firebase_token(Authorization: str = Header(...)) -> str:
    id_token = Authorization.replace("Bearer ", "")
    try:
        # Verify the ID token while checking if the token is revoked by
        # passing check_revoked=True.
        decoded_token = auth.verify_id_token(id_token, check_revoked=True)
        # Token is valid and not revoked.
        uid = decoded_token["uid"]
        return uid
    except ValueError:
        # Token was invalid or revoked.
        raise HTTPException(status_code=401, detail="Token was invalid or revoked")
