from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    URL_21: str
    URL_20: str
    URL_to: str
    GUARANTEE_URL: str
    USER_1: str
    USER_2: str
    USER_3: str
    USER_4: str
    USER_5: str

    class Config:
        env_file = ".env"


settings = Settings(_env_file="../credentials/.env")

print(":")