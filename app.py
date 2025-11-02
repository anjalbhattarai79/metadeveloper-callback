import os
import requests
from fastapi import FastAPI

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")


app = FastAPI()

@app.get("/instagram/callback")
async def instagram_callback(code: str):
    # Exchange code for access token
    response = requests.post(
        "https://api.instagram.com/oauth/access_token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code
        }
    )
    token_data = response.json()
    return token_data
