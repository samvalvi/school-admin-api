from os import getenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from db.config import Base, engine
from routes.admin_router import admin_router
from routes.course_router import course_router
from routes.student_router import student_router
from routes.teacher_router import teacher_router
from routes.login_router import login_router
from dotenv import load_dotenv

Base.metadata.create_all(bind=engine)
load_dotenv(getenv('ENV_FILE'))


app = FastAPI(
    title="School Management API",
    description="School Management API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=getenv('CORS_ORIGIN_WHITELIST'),
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

app.include_router(prefix="/login", router=login_router)
app.include_router(prefix="/student", router=student_router)
app.include_router(prefix="/course", router=course_router)
app.include_router(prefix="/teacher", router=teacher_router)
app.include_router(prefix="/admin", router=admin_router)


@app.get("/", tags=["Home"])
def root():
    return {
                "message": "School api",
                "version": "1.0.0",
                "author": "Samuel"
            }
