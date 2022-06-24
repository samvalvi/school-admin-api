from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from db.config import get_db
from schemas.teacher import Teacher, CreateTeacher, TeacherDetail
from repository import teacher as crud
from repository import course as crud_course


teacher_router = APIRouter()


@teacher_router.get("/get/teachers", response_model=list[Teacher], tags=["Teacher"], status_code=status.HTTP_200_OK)
def get_teachers(session: Session = Depends(get_db)):
    teachers = crud.get_teachers(session)
    return teachers


@teacher_router.get("/get/teacher/{_id}", response_model=TeacherDetail, tags=["Teacher"], status_code=status.HTTP_200_OK)
def get_teacher_by_id(_id: str, session: Session = Depends(get_db)):
    teacher = crud.get_teacher_by_id(_id, session)

    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    return teacher


@teacher_router.post("/create/teacher", response_model=Teacher, tags=["Teacher"], status_code=status.HTTP_200_OK)
async def create_teacher(teacher: CreateTeacher, session: Session = Depends(get_db)):
    existing_teacher = crud.get_teacher_by_email(teacher.email, session)

    if existing_teacher:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Teacher already exists")

    result = await crud.create_teacher(teacher, session)
    return result


@teacher_router.put("/update/teacher/{_id}", response_model=Teacher, tags=["Teacher"], status_code=status.HTTP_200_OK)
async def update_teacher(_id: str, teacher: CreateTeacher, session: Session = Depends(get_db)):
    existing_teacher = crud.get_teacher_by_id(_id, session)

    if not existing_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    result = await crud.update_teacher(_id, teacher, session)
    return result


@teacher_router.delete("/delete/teacher/{_id}", tags=["Teacher"], status_code=status.HTTP_200_OK)
async def delete_teacher(_id: str, session: Session = Depends(get_db)):
    existing_teacher = crud.get_teacher_by_id(_id, session)

    if not existing_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    await crud.delete_teacher(_id, session)
    return {"message": "Teacher deleted"}


@teacher_router.post("/add/course/{_id}", tags=["Teacher"], status_code=status.HTTP_200_OK)
async def add_course(_id: str, course_id: str, session: Session = Depends(get_db)):
    existing_teacher = crud.get_teacher_by_id(_id, session)

    if not existing_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    existing_course = crud_course.get_course_by_id(session, course_id)

    if not existing_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    await crud.add_course(_id, course_id, session)
    return {"message": "Course added"}
