from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
import requests
import json


from app.schemas.users import UserCredentials
from app.db import get_db as db
from app.core.security import get_user_token
from app.services.auth import AuthService
from app.core.dependecies import include_auth
from app.models import User
from app.core.utils import ResponseHandler, Custom
from app.core.config import settings


router = APIRouter()


# user signup endpoint
@router.post('/signup')
async def user_signup(credentials: UserCredentials, db: Session = Depends(db)):
  return await AuthService.signup(credentials, db)


# user login endpoint
@router.post('/login')
async def user_login(credentials: UserCredentials, db: Session = Depends(db)):
  return await AuthService.login(credentials, db)


# generate new user token using refresh token
@router.get("/token/refresh")
async def read_items(
  user: User = Depends(include_auth)
):
  try:
    result = await get_user_token(user, f'successfully generated new token for user-{user.id}!', 200)
    return result
  except Exception:
    raise ResponseHandler.invalid_token()
  


# handle google concent page
@router.get("/google")
async def user_google_auth(state: str):
  url = (
    f"https://accounts.google.com/o/oauth2/v2/auth"
    f"?scope=openid email profile"
    f"&access_type=offline"
    f"&response_type=code"
    f"&state={state}"
    f"&redirect_uri={settings.google_redirect_uri}"
    f"&client_id={settings.google_client_id}"
  )
  
  return RedirectResponse(url)


# handle google callback
@router.get('/google/callback')
async def user_google_callback(state, code: str | None = None, error: str | None = None, db: Session = Depends(db)):
  token_url = "https://accounts.google.com/o/oauth2/token"
  payload = {
    "code": code,
    "client_id": settings.google_client_id,
    "client_secret": settings.google_client_secret,
    "redirect_uri": settings.google_redirect_uri,
    "grant_type": "authorization_code",
  }
 
  if error:
    raise ResponseHandler.unauthorized(f"something went wrong try again - mostly {Custom.snake_to_title(error)}!")

  # get user google token
  response = requests.post(token_url, data=payload)
  access_token = response.json().get("access_token")

  # request for user informations
  user_info = requests.get(
    "https://www.googleapis.com/oauth2/v1/userinfo", 
    headers={"Authorization": f"Bearer {access_token}"}
  )
  
  # retrive the user informations 
  user_data = user_info.json()
  email = user_data.get('email')
  name = user_data.get('name')
  img_src = user_data.get('picture')

  print(user_data)

  # extract the state params from the url 
  state = json.loads(state)
  source_tag = state.get("source", "")
  
  # check if the google account is verified or not 
  if not user_data.get("verified_email", False):
    raise ResponseHandler.unauthorized(f"{email} is not a verified google account!")
  
  payload = {
    "name": name,
    "email": email,
    "picture": img_src,
  }

  return await AuthService.google_auth(payload, source_tag, db)

  