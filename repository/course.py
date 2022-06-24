from sqlalchemy.orm import Session
from models.model import Course
from schemas.course import CreateCourse
from uuid import uuid4


def get_courses(session: Session):
    query = session.query(Course).all()
    return query


def get_course_by_id(session: Session, _id: str):
    query = session.query(Course).filter_by(course_id=_id).first()
    return query


def get_course_by_name(session: Session, _name: str):
    query = session.query(Course).filter_by(course_name=_name).first()
    return query


async def create_course(session: Session, course: CreateCourse):
    course_id = str(uuid4())
    query = Course(course_id=course_id, course_name=course.course_name, course_description=course.course_description)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query


async def update_course(session: Session, _id: str, course: CreateCourse):
    query = await session.query(Course).filter_by(course_id=_id).first()
    query.course_name = course.course_name
    query.course_description = course.course_description
    session.commit()
    session.refresh(query)
    return query


async def delete_course(session: Session, _id: str):
    query = session.query(Course).filter_by(course_id=_id).first()
    session.delete(query)
    session.commit()
