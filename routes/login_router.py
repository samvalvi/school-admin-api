from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException
from db.config import get_db
from schemas import token_schema
from services.auth_service import authenticate_user, create_access_token


login_router = APIRouter()


@login_router.post("/login", tags=["Login"],
                   status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.student_id or user.teacher_id or user.admin_id})
    return {"access_token": access_token, "token_type": "bearer"}
