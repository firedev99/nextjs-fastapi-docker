from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware

from app.routers import patients, auth, health, hospital, doctor
from app.routers.admin import patients as patients_admin, users, hospitals as hospitals_admin, doctors as doctors_admin
from app.core.security import origins
from app.core.dependecies import include_admin

version = 'v1'

app = FastAPI(
  root_path=f'/api/{version}',
  docs_url=f"/docs", openapi_url=f"/openapi.json",
  title='Gluco Guide Backend',
  version=version,
  contact={
    "name": "firedev99",
    "email": "firethedev@gmail.com"
  }
)


app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# custom exception handler 
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(_: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={
      "status": "unsuccessful",
      "message": exc.detail
    }
  )


# general routes 
app.include_router(auth.router, prefix=f'/auth', tags=['Users / Auth'])
app.include_router(hospital.router, prefix=f'/hospitals', tags=['General / Hospitals'])
app.include_router(doctor.router, prefix=f'/users/doctors', tags=['General / Doctors'])


# patient routes 
app.include_router(patients.router, prefix=f'/users/patients', tags=['Patient / Profile'])
app.include_router(health.router, prefix=f'/users/patients/health', tags=['Patient / Health Monitoring Records'])


# admin routes 
app.include_router(users.router, prefix=f'/admin/users', tags=['Admin / Users'], dependencies=[Depends(include_admin)])
app.include_router(patients_admin.router, prefix=f'/admin/users/patients', tags=['Admin / Patients'], dependencies=[Depends(include_admin)])
app.include_router(doctors_admin.router, prefix=f'/admin/users/doctors', tags=['Admin / Doctors'], dependencies=[Depends(include_admin)])
app.include_router(hospitals_admin.router, prefix=f'/admin/hospitals', tags=['Admin / Hospitals'], dependencies=[Depends(include_admin)])



