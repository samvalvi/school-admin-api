from uuid import uuid4
from sqlalchemy.orm import Session
from models.model import Student, Course
from schemas.student import CreateStudent
from bcrypt import hashpw, gensalt


def get_students(session: Session):
    query = session.query(Student).all()
    return query


def get_student_by_id(_id: str, session: Session):
    query = session.query(Student).filter_by(student_id=_id).first()
    return query


def get_student_by_email(_email: str, session: Session):
    query = session.query(Student).filter_by(email=_email).first()
    return query


async def create_student(student: CreateStudent, session: Session):
    _id = str(uuid4())
    password = hashpw(student.password.encode('utf-8'), gensalt())

    query = Student(student_id=_id, first_name=student.first_name, last_name=student.last_name,
                    email=student.email, age=student.age, password=password)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query


async def update_student(_id: str, student: CreateStudent, session: Session):
    query = await session.query(Student).filter_by(student_id=_id).first()
    query.first_name = student.first_name
    query.last_name = student.last_name
    query.email = student.email
    query.age = student.age

    session.commit()
    session.refresh(query)
    return query


async def delete_student(_id: str, session: Session):
    query = session.query(Student).filter_by(student_id=_id).first()
    session.delete(query)
    session.commit()


async def add_course(_id: str, course_id: str, session: Session):
    student = session.query(Student).filter_by(student_id=_id).first()
    course = session.query(Course).filter_by(course_id=course_id).first()
    course.students.append(student)
    session.add(course)
    session.commit()
