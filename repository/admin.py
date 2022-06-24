from sqlalchemy.orm import Session
from models.model import Admin
from bcrypt import hashpw, gensalt
from uuid import uuid4
from schemas.admin import CreateAdmin


def get_admins(session: Session):
    query = session.query(Admin).all()
    return query


def get_admin_by_id(session: Session, _id: str):
    query = session.query(Admin).filter_by(admin_id=_id).first()
    return query


def get_admin_by_email(session: Session, _email: str):
    query = session.query(Admin).filter_by(email=_email).first()
    return query


async def create_admin(session: Session, _admin: CreateAdmin):
    admin_id = str(uuid4())
    admin_password = hashpw(_admin.password.encode('utf-8'), gensalt())
    query = Admin(admin_id=admin_id, first_name=_admin.first_name, last_name=_admin.last_name,
                  email=_admin.email, password=admin_password)
    session.add(query)
    session.commit()
    session.refresh(query)
    return query


async def update_admin(session: Session, _admin: CreateAdmin, _id: str):
    query = session.query(Admin).filter_by(admin_id=_id).first()
    query.first_name = _admin.first_name
    query.last_name = _admin.last_name
    query.email = _admin.email
    session.commit()
    session.refresh(query)
    return query


async def delete_admin(session: Session, _id: str):
    query = session.query(Admin).filter_by(admin_id=_id).first()
    session.delete(query)
    session.commit()
