from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from db.config import get_db
from schemas.admin import Admin, CreateAdmin
from repository import admin as crud


admin_router = APIRouter()


@admin_router.get("/get/admins", response_model=list[Admin], tags=["Admin"], status_code=status.HTTP_200_OK)
def get_courses(session: Session = Depends(get_db)):
    query = crud.get_admins(session)
    return query


@admin_router.get("/get/admin/{_id}", response_model=Admin, tags=["Admin"], status_code=status.HTTP_200_OK)
def get_admin_by_id(_id: str, session: Session = Depends(get_db)):
    query = crud.get_admin_by_id(session, _id)

    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    return query


@admin_router.post("/create/admin", response_model=Admin, tags=["Admin"], status_code=status.HTTP_200_OK)
async def create_admin(admin_: CreateAdmin, session: Session = Depends(get_db)):
    existing_admin = crud.get_admin_by_email(session, admin_.email)

    if existing_admin:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Admin already exists")

    query = await crud.create_admin(session, admin_)
    return query


@admin_router.put("/update/admin/{_id}", response_model=Admin, tags=["Admin"], status_code=status.HTTP_200_OK)
async def update_admin(_id: str, admin_: CreateAdmin, session: Session = Depends(get_db)):
    existing_admin = crud.get_admin_by_id(session, _id)

    if not existing_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    query = await crud.update_admin(session, admin_, _id)
    return query


@admin_router.delete("/delete/admin/{_id}", tags=["Admin"], status_code=status.HTTP_200_OK)
async def delete_admin(_id: str, session: Session = Depends(get_db)):
    existing_admin = crud.get_admin_by_id(session, _id)

    if not existing_admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin not found")

    query = await crud.delete_admin(session, _id)
    return {"message": "Admin deleted"}
