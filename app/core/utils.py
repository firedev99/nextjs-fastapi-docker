from fastapi import HTTPException
import uuid 

class Custom:
  @staticmethod
  def snake_to_title(snake_str: str):
    return ' '.join(word.capitalize() for word in snake_str.split('_'))
  

class ResponseHandler:
  @staticmethod
  def invalid_token():
    raise HTTPException(
      status_code=401, 
      detail=f'invalid token!', 
      headers={"WWW-Authenticate": "Bearer"}
    )
  
  @staticmethod
  def not_found_error(warning=""):
    raise HTTPException(
      status_code=404,
      detail=f'{warning}'
    )
  
  @staticmethod
  def unauthorized(message: str):
    raise HTTPException(
      status_code=401,
      detail=f"{message}"
    )
  
  @staticmethod
  def no_permission(message: str):
    raise HTTPException(
      status_code=403,
      detail=f"{message}"
    )
  


