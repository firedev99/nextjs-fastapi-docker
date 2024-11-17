import jwt
import bcrypt
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import base64
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from sqlalchemy.orm import Session, defer
from uuid import UUID

from app.models import User, Patient, Doctor
from app.core.config import settings
from app.core.utils import ResponseHandler



origins = [origin.strip() for origin in settings.frontend_origins.split(",")]



# generate a hashed password
def generate_hash(text: str) -> str:
  salt = bcrypt.gensalt()
  hashed_text = bcrypt.hashpw(text.encode(), salt)
  return hashed_text.decode()



# verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
  password_byte_enc = plain_password.encode() #convert password to bytes
  hashed_byte_enc = hashed_password.encode() # convert hashed string to bytes 
  return bcrypt.checkpw(password_byte_enc, hashed_byte_enc)



# encrypt a plain text using AES in GCM mode
def encrypt(plain_text: str, key=settings.hashing_secret_key):
  secret_key = base64.b64decode(key)
  iv = get_random_bytes(12)
  cipher = AES.new(secret_key, AES.MODE_GCM, nonce=iv)
  ciphertext, tag = cipher.encrypt_and_digest(plain_text.encode())
  return base64.b64encode(iv + ciphertext + tag).decode()



# decrypt and autheticate an encrypted content using AES in GCM mode (AEAD)
async def decrypt(encrypted_text: str, key=settings.hashing_secret_key):
  try:
    # convert the key n encryption into bytes 
    secret_key = base64.b64decode(key)
    encrypted_data = base64.b64decode(encrypted_text)
    # extract iv, ciphertext n tag 
    iv = encrypted_data[:12]  # first 12 bytes for iv
    ciphertext = encrypted_data[12:-16]  # middle part for ciphertext
    tag = encrypted_data[-16:] # last 16 bytes is the tag 
    # create the cipher 
    cipher = AES.new(secret_key, AES.MODE_GCM, nonce=iv)
    # decrypt and verify the ciphertext 
    decrypted_content_byte = cipher.decrypt_and_verify(ciphertext, tag)

    return decrypted_content_byte.decode()
  except (UnicodeDecodeError, ValueError, KeyError) as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"decryption failed {e}")


# covert uuid string to short url
def uuid_to_short_url(uuid_str: str):
  try:
    uuid_bytes = UUID(uuid_str).bytes # convert to byes
    # encode bytes to base64 string
    base64_str = base64.urlsafe_b64encode(uuid_bytes).rstrip(b'=').decode('ascii')
    
    return base64_str
  except Exception:
    raise HTTPException(
      status_code=400,
      detail='failed to generate url using uuid!'
    )


# convert short url to original uuid
def short_url_to_uuid(short_url: str):
  try:
    padding = '=' * (4 - len(short_url) % 4)
    base64_str = short_url + padding 
    uuid_bytes = base64.urlsafe_b64decode(base64_str) # decode base64 string to bytes

    return UUID(bytes=uuid_bytes) # original uuid
  except Exception:
    raise HTTPException(
      status_code=400,
      detail='failed to decode the uuid generated url!'
    ) 
  


# create new token
def create_access_token(data: dict, expires_delta: datetime) -> str:
  payload = data.copy()
  payload['iat'] = datetime.now(timezone.utc)
  payload['exp'] = expires_delta

  return jwt.encode(payload, settings.jwt_secret_key)



# decode the token 
def decode_token(token: str):
  try:
    return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
  except InvalidTokenError:
    raise ResponseHandler.invalid_token()
  except ExpiredSignatureError:
    raise ResponseHandler.invalid_token()



# verify is the token is valid 
def verify_token(token: str, db: Session):
  payload = decode_token(token)
  user_id = payload.get('sub', None)
    
  # check if token payload has the id
  if not user_id:
    raise ResponseHandler.invalid_token()
  
  # get user w/o passwords, created n updated times 
  user = db.query(User).filter(User.id == user_id).options(defer(User.password)).first()

  # check if the user exists
  if not user:
    raise ResponseHandler.invalid_token()
  
  return user



# get user access token
async def get_user_token(user: User | Patient | Doctor, message: str, status_code: int):
  payload = { "sub": f'{user.id}'}

  # generate the token exipirations
  access_token_expires = datetime.now(timezone.utc) + timedelta(minutes=15) + timedelta(minutes=settings.access_token_expires)
  refresh_token_expires = datetime.now(timezone.utc) + timedelta(minutes=15) + timedelta(days=settings.refresh_token_expires)

  # create access n refresh tokens
  access_token = create_access_token(payload, access_token_expires)
  refresh_token = create_access_token(payload, refresh_token_expires)

  # generated short url using user id 
  url = uuid_to_short_url(str(user.id)) 
  
  response = JSONResponse(
    content={
      "status": "successful",
      "message": message,
      "data": {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
          "url": url,
          "name": user.name,
          "email": user.email,
          "role": user.role,
        }
      }
    },
    status_code=status_code
  )

  return response
