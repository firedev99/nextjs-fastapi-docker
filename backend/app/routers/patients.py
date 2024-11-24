from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import Patient
from app.db import get_db as db
from app.core.dependecies import include_auth
from app.services.patient import PatientService
from app.schemas.users import UserUpdate, UserPasswordChange
from app.schemas.health import HealthRecordUpdate


router = APIRouter()


# get a patient profile information by id 
@router.get("/profile")
async def get_patient_account_information(id: str, session_user: Patient = Depends(include_auth)):
  return await PatientService.get_patient_information(id, session_user)
    


# change a patient profile information by id
@router.put("/profile")
async def update_patient_account_information(
  id: str, 
  updated_data: UserUpdate, 
  db: Session = Depends(db), 
  session_user: Patient = Depends(include_auth)
):
  return await PatientService.change_patient_information(id, updated_data, session_user, db)
  


# change user password 
@router.put("/profile/password")
async def change_patient_account_password(
  updated_data: UserPasswordChange, 
  db: Session = Depends(db), 
  session_user: Patient = Depends(include_auth)
):
  try:
    return await PatientService.change_user_password(updated_data, session_user, db)
  except Exception:
    raise HTTPException(status_code=403, detail="you're not allowed to change the password!")

