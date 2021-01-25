from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
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

    class Config:
        env_file = None


settings = Settings(_env_file="./credentials/.env")

TOKEN = settings.TOKEN
URL_21 = settings.URL_21
URL_20 = settings.URL_20
URL_TO = settings.URL_to
GUARANTEE_URL = settings.GUARANTEE_URL
WEBHOOK_URL = settings.WEBHOOK_URL
USER_1 = settings.USER_1
USER_2 = settings.USER_2
USER_3 = settings.USER_3
USER_4 = settings.USER_4
USER_5 = settings.USER_5
WHITE_LIST = [
    USER_1,
    USER_2,
    USER_3,
    USER_4,
    USER_5,
]

