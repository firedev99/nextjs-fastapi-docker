from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app.models import User, Patient
from app.core.utils import ResponseHandler
from app.schemas.users import UserCredentials, UserLoginGoogle
from app.core.security import decrypt, generate_hash, verify_password, get_user_token



class AuthService:
  @staticmethod
  async def signup(credentials: UserCredentials, db: Session):
    exits = db.query(User).where(User.email == credentials.email).first()
    
    # check if the user exists
    if exits:
      raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'user w email: {credentials.email} already exists!')
    
    # decrypt the password from the client 
    decrypted_password = await decrypt(credentials.password)

    # generate hashed password
    hashed_password = generate_hash(decrypted_password)
    credentials.password = hashed_password

    # create a patient w the hashed password
    new_patient = Patient(**credentials.model_dump())
    db.add(new_patient)
    db.commit()
    
    db.refresh(new_patient)

    # return user details w token
    return await get_user_token(new_patient, f'patient-{new_patient.id} has been created successfully!', status.HTTP_201_CREATED)

  

  # handle built in login 
  @staticmethod
  async def login(credentials: UserCredentials, db: Session):
    user = db.query(User).filter(User.email == credentials.email).first()
    
    # check if the user exists
    if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials!')

    # decrypt the password from the client 
    decrypted_password = await decrypt(credentials.password)
    
    # verify password 
    if not verify_password(decrypted_password, user.password):
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='password is incorrect')
    

    # return user details w token
    return await get_user_token(user, f'{user.id} - login successful!', status.HTTP_200_OK)
  


  # handle google authetication (patient)
  @staticmethod
  async def google_auth(credentials: UserLoginGoogle, tag: str | None, db: Session):
    email = credentials.get('email')
    name = credentials.get('name')
    img_src = credentials.get('picture')

    if tag not in ["gg_login", "gg_signup"]: # allow only custom context 
      raise HTTPException(
        status_code=400,
        detail=f"{tag} is not a valid context!"
      )
    
    # get the user using the payload email 
    user = db.query(User).where(User.email == email).first()

    # handle user login
    # verify if the user exists 
    if tag == "gg_login" and not user:
      raise ResponseHandler.unauthorized(f"{email} - havent signed up yet!")
    
    
    # if the user is verified then directly return the tokens 
    if tag == "gg_login" and user:
      return await get_user_token(user, f'{user.id} - login successful via google!', 200)
        

    # handle user signup
    # if the user already exists directly return the tokens  
    if tag == "gg_signup" and user:
      return await get_user_token(user, f'{user.id} - new account created using google!', 201)
        
    # create a new patient 
    new_patient = Patient(
      email=email,
      name=name,
      img_src=img_src
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    # return the tokens for the newly created user
    return await get_user_token(new_patient, f'patient-{new_patient.id} has been created successfully!', 201)
      