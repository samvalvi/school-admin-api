from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from db.config import get_db
from schemas.student import Student, CreateStudent, StudentDetail
from repository import student as crud
from repository import course as crud_course


student_router = APIRouter()


@student_router.get("/get/students", response_model=list[Student], tags=["Student"], status_code=status.HTTP_200_OK)
def get_students(session: Session = Depends(get_db)):
    students = crud.get_students(session)
    return students


@student_router.get("/get/student/{_id}", response_model=StudentDetail, tags=["Student"], status_code=status.HTTP_200_OK)
def get_student_by_id(_id: str, session: Session = Depends(get_db)):
    student = crud.get_student_by_id(_id, session)

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    return student


@student_router.post("/create/student", response_model=Student, tags=["Student"], status_code=status.HTTP_200_OK)
async def create_student(student: CreateStudent, session: Session = Depends(get_db)):
    existing_student = crud.get_student_by_email(student.email, session)

    if existing_student:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student already exists")

    student = await crud.create_student(student, session)
    return student


@student_router.put("/update/student/{_id}", response_model=Student, tags=["Student"], status_code=status.HTTP_200_OK)
async def update_student(_id: str, student: CreateStudent, session: Session = Depends(get_db)):
    existing_student = crud.get_student_by_id(_id, session)

    if not existing_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    student = await crud.update_student(_id, student, session)
    return student


@student_router.delete("/delete/student/{_id}", tags=["Student"], status_code=status.HTTP_200_OK)
async def delete_student(_id: str, session: Session = Depends(get_db)):
    existing_student = crud.get_student_by_id(_id, session)

    if not existing_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    await crud.delete_student(_id, session)
    return {"message": "Student deleted"}


@student_router.post("/add/course/{_id}/{course_id}", tags=["Student"], status_code=status.HTTP_200_OK)
async def add_course(_id: str, course_id: str, session: Session = Depends(get_db)):
    existing_student = crud.get_student_by_id(_id, session)

    if not existing_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    existing_course = crud_course.get_course_by_id(session, course_id)

    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    student = await crud.add_course(_id, course_id, session)
    return {"message": "Course added"}
