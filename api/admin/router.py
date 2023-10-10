import os

import requests
from fastapi import APIRouter
from firebase_admin import auth

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def exchange_custom_token_for_id_token(custom_token):
    API_KEY = os.environ.get("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={API_KEY}"
    data = {"token": custom_token, "returnSecureToken": True}
    r = requests.post(url, json=data)
    id_token = r.json().get("idToken")

    return id_token


@router.get("/get_custom_token")
def get_custom_token(user_id: str = "aeANvF2kQoQVUT3GK7biyV1MtFf2"):
    custom_token = auth.create_custom_token(user_id)
    token = exchange_custom_token_for_id_token(custom_token.decode())
    return token
