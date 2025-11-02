import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
from dotenv import load_dotenv

load_dotenv()  # load .env variables

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


@app.get("/", response_class=HTMLResponse)
async def home():
    auth_url = (
        f"https://www.instagram.com/oauth/authorize"
        f"?force_reauth=true&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=instagram_business_basic,"
        f"instagram_business_manage_messages,"
        f"instagram_business_manage_comments,"
        f"instagram_content_publish,"
        f"instagram_business_manage_insights"
    )
    return f'<h2>Instagram OAuth Test</h2><a href="{auth_url}">Login with Instagram</a>'


@app.get("/instagram/callback")
async def instagram_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code found in callback"}

    # Exchange code for access token
    token_url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return {"error": "Failed to get access token", "details": response.json()}

    access_token_data = response.json()
    return {
        "message": "Access token obtained successfully",
        "access_token_data": access_token_data
    }


# Optional: handle HEAD requests to prevent 405 errors
@app.head("/instagram/callback")
async def head_callback():
    return ""
