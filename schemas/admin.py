from pydantic import BaseModel


class AdminBase(BaseModel):
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class CreateAdmin(AdminBase):
    password: str


class Admin(AdminBase):
    admin_id: str

    class Config:
        orm_mode = True
