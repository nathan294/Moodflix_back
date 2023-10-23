import os

import requests
from firebase_admin import auth


def exchange_custom_token_for_id_token(custom_token):
    API_KEY = os.environ.get("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key={API_KEY}"
    data = {"token": custom_token, "returnSecureToken": True}
    r = requests.post(url, json=data)
    id_token = r.json().get("idToken")

    return id_token


def delete_firebase_user(firebase_id: str) -> None:
    try:
        auth.delete_user(firebase_id)
        print(f"Successfully deleted user with Firebase ID: {firebase_id}")
    except auth.UserNotFoundError:
        print(f"User with Firebase ID {firebase_id} not found")
    except Exception as e:
        print(f"An error occurred: {e}")
