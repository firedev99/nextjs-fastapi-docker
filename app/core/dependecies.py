from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import verify_token
from app.core.utils import ResponseHandler
from app.db import get_db
from sqlalchemy.orm import Session

from app.models import Patient

oauth2_scheme = HTTPBearer()

def include_auth(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
  if credentials.scheme != "Bearer":
    raise ResponseHandler.invalid_token()
  
  user = verify_token(credentials.credentials, db)
  
  if not user:
    raise ResponseHandler.invalid_token()
  
  patient = db.query(Patient).where(Patient.id == user.id).first()

  if not patient:
    raise HTTPException(
      status_code=400,
      detail='something went wrong!'
    )
  
  return patient


def include_admin(db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
  if credentials.scheme != "Bearer":
    raise ResponseHandler.invalid_token()
  
  user = verify_token(credentials.credentials, db)
  
  if not user:
    raise ResponseHandler.invalid_token()
  
  
  if not user.role == "admin":
    raise ResponseHandler.no_permission(f'user-{user.id} does not have permission!')
  
  return user 