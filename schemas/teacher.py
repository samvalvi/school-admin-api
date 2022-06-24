from typing import List
from pydantic import BaseModel


class TeacherBase(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class CreateTeacher(TeacherBase):
    password: str

    class Config:
        orm_mode = True


class Teacher(TeacherBase):
    teacher_id: str

    class Config:
        orm_mode = True


class CourseList(BaseModel):
    course_id: str

    class Config:
        orm_mode = True


class TeacherDetail(TeacherBase):
    teacher_id: str
    courses: List[CourseList] = []

    class Config:
        orm_mode = True
