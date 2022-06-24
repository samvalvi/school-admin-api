from sqlalchemy import String, Column, Integer, LargeBinary, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.config import Base


class Student(Base):
    __tablename__ = 'students'
    student_id = Column(String(255), primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    password = Column(LargeBinary(255), nullable=False)
    role = Column(String(255), default='student')
    is_active = Column(Boolean, default=False)
    courses = relationship('Course', secondary='student_courses', back_populates='students')


class StudentCourses(Base):
    __tablename__ = 'student_courses'
    student_id = Column(String(255), ForeignKey('students.student_id'), primary_key=True)
    course_id = Column(String(255), ForeignKey('courses.course_id'), primary_key=True)


class TeacherCourses(Base):
    __tablename__ = 'teacher_courses'
    teacher_id = Column(String(255), ForeignKey('teachers.teacher_id'), primary_key=True)
    course_id = Column(String(255), ForeignKey('courses.course_id'), primary_key=True)


class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(String(255), primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(LargeBinary(255), nullable=False)
    role = Column(String(255), default='teacher')
    is_active = Column(Boolean, default=False)
    courses = relationship('Course', secondary='teacher_courses', back_populates='teachers')


class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(String(255), primary_key=True)
    course_name = Column(String(255), nullable=False)
    course_description = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    students = relationship("Student", secondary="student_courses", back_populates="courses", single_parent=True, cascade="all, delete-orphan")
    teachers = relationship("Teacher", secondary="teacher_courses", back_populates="courses", single_parent=True, cascade="all, delete-orphan")


class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(String(255), primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(LargeBinary(255), nullable=False)
    role = Column(String(255), default='admin')
    is_active = Column(Boolean, default=False)
