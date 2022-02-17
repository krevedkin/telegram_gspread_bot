# script version 1.3
from pydantic import BaseSettings
import os

basedir = os.path.abspath(os.path.dirname(__file__))
path_to_env = os.path.join(basedir, "credentials/.env")
path_to_creds = os.path.join(basedir, "credentials/credentials.json")


class Settings(BaseSettings):
    TOKEN: str
    URL_TEST: str
    URL_22: str
    URL_21: str
    URL_20: str
    URL_to: str
    GUARANTEE_URL: str
    WEBHOOK_URL: str
    USER_1: str
    USER_2: str
    USER_3: str
    USER_4: str
    USER_5: str
    USER_6: str
    USER_7: str
    USER_8: str

    class Config:
        env_file = path_to_env


settings = Settings()
