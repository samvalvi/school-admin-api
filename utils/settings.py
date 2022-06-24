from os import getenv
from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv(getenv('ENV_FILE'))


class Settings(BaseSettings):

    secret_key = getenv('SECRET_KEY')
    algorithm = getenv('ALGORITHM')
    expires = getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
