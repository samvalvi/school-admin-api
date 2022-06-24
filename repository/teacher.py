from sqlalchemy.orm import Session
from models.model import Teacher, Course
from schemas.teacher import CreateTeacher
from uuid import uuid4
from bcrypt import hashpw, gensalt


def get_teachers(session: Session):
    query = session.query(Teacher).all()
    return query


def get_teacher_by_id(_id: str, session: Session):
    query = session.query(Teacher).filter_by(teacher_id=_id).first()
    return query


def get_teacher_by_email(_email: str, session: Session):
    query = session.query(Teacher).filter_by(email=_email).first()
    return query


async def create_teacher(teacher: CreateTeacher, session: Session):
    teacher_id = str(uuid4())
    password = hashpw(teacher.password.encode('utf-8'), gensalt())

    query = Teacher(teacher_id=teacher_id, first_name=teacher.first_name, last_name=teacher.last_name,
                    email=teacher.email, password=password)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query


async def update_teacher(_id: str, teacher: CreateTeacher, session: Session):
    query = await session.query(Teacher).filter_by(teacher_id=_id).first()
    query.first_name = teacher.first_name
    query.last_name = teacher.last_name
    query.email = teacher.email

    session.commit()
    session.refresh(query)
    return query


async def delete_teacher(_id: str, session: Session):
    query = await session.query(Teacher).filter_by(teacher_id=_id).first()
    session.delete(query)
    session.commit()


async def add_course(_id: str, course_id: str, session: Session):
    teacher = session.query(Teacher).filter_by(teacher_id=_id).first()
    course = session.query(Course).filter_by(course_id=course_id).first()
    course.teachers.append(teacher)
    session.add(course)
    session.commit()
