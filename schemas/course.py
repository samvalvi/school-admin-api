from typing import List
from pydantic import BaseModel


class CourseBase(BaseModel):
    course_name: str
    course_description: str

    class Config:
        orm_mode = True


class CreateCourse(CourseBase):
    pass

    class Config:
        orm_mode = True


class Course(CourseBase):
    course_id: str

    class Config:
        orm_mode = True


class TeacherCourse(BaseModel):
    teacher_id: str

    class Config:
        orm_mode = True


class CourseDetail(CourseBase):
    course_id: str
    teachers: List[TeacherCourse] = []

    class Config:
        orm_mode = True
