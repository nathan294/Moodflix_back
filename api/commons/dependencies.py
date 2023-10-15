from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from api.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


security = HTTPBearer()


def verify_firebase_token(authorization: HTTPAuthorizationCredentials = Security(security)) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    # Get Token from header
    id_token = authorization.credentials
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
