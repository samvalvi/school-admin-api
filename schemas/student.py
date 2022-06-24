from typing import List
from pydantic import BaseModel


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int

    class Config:
        orm_mode = True


class CreateStudent(StudentBase):
    password: str

    class Config:
        orm_mode = True


class Student(StudentBase):
    student_id: str

    class Config:
        orm_mode = True


class CourseList(BaseModel):
    course_id: str

    class Config:
        orm_mode = True


class StudentDetail(StudentBase):
    student_id: str
    courses: List[CourseList] = []

    class Config:
        orm_mode = True
