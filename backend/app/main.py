from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware

from app.routers import patients, auth, health, hospital, doctor
from app.routers.admin import patients as patients_admin, users, hospitals as hospitals_admin, doctors as doctors_admin
from app.core.security import origins
from app.core.dependecies import include_admin

from app.core.config import settings
from app.workers.celery import celery
from app.workers.tasks import send_email_task

import httpx
import json
from app.core.dependecies import cache 
from app.core.utils import ResponseHandler
from redis import Redis


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


# redis caching tesing api
@app.get('/redis/dogs')
async def read_redis_entries(
  redis: Redis = Depends(cache)
):
  http_client = httpx.AsyncClient()
  result = redis.get('dogs_api_all')

  if not result:
    response = await http_client.get('https://dog.ceo/api/breeds/list/all')
    result = response.json()

    json_data = json.dumps(result)
    redis.set('dogs_api_all', json_data)
    
    return ResponseHandler.fetch_successful('successfully retrieved dogs data!', result)

  return ResponseHandler.fetch_successful('sucessfully retrieve dogs data from redis caching!', json.loads(result))
 

# celery tasks testing apis 
@app.get('/send-email')
async def run_task():
  task = send_email_task.apply_async(
    args=("sauravagun1999@gmail.com", "GlucoGuide Email Tasks", "Testing SMTP Connection!"),
    countdown=60
  )
  return { "status": "successful", "message": f"successfully, sent mail from {settings.owner_email}", "tast_id": task.id }


# query a celery task w task id 
@app.get('/tasks/{task_id}')
async def get_task_status(task_id: str):
  task = celery.AsyncResult(task_id)
  return { "task_id": task_id, "status": task.status, "result": task.result }



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



