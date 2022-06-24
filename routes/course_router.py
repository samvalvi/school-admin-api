from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from db.config import get_db
from schemas.course import Course, CreateCourse, CourseDetail
from repository import course as crud


course_router = APIRouter()


@course_router.get("/get/courses", response_model=list[Course], tags=["Course"], status_code=status.HTTP_200_OK)
def get_courses(session: Session = Depends(get_db)):
    query = crud.get_courses(session)
    return query


@course_router.get("/get/course/{_id}", response_model=CourseDetail, tags=["Course"], status_code=status.HTTP_200_OK)
def get_course_by_id(_id: str, session: Session = Depends(get_db)):
    query = crud.get_course_by_id(session, _id)

    if not course_router:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    return query


@course_router.post("/create/course", response_model=Course, tags=["Course"], status_code=status.HTTP_200_OK)
async def create_course(course_: CreateCourse, session: Session = Depends(get_db)):
    existing_course = crud.get_course_by_name(session, course_.course_name)

    if existing_course:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course already exists")

    query = await crud.create_course(session, course_)
    return query


@course_router.put("/update/course/{_id}", response_model=Course, tags=["Course"], status_code=status.HTTP_200_OK)
async def update_course(_id: str, course_: CreateCourse, session: Session = Depends(get_db)):
    existing_course = crud.get_course_by_id(session, _id)

    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    query = await crud.update_course(session, _id, course_)
    return query


@course_router.delete("/delete/course/{_id}", tags=["Course"], status_code=status.HTTP_200_OK)
async def delete_course(_id: str, session: Session = Depends(get_db)):
    existing_course = crud.get_course_by_id(session, _id)

    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    query = await crud.delete_course(session, _id)
    return {"message": "Course deleted"}
