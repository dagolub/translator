from typing import Optional

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "Translator"
    PROJECT_NAME: str = "Translator"
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "email-templates/build"
    EMAILS_ENABLED: bool = True
    EMAILS_FROM_NAME: str = "Info"
    EMAIL_TEST_USER: str
    EMAILS_FROM_EMAIL: str = ""
    SMTP_TLS: bool = True

    SMTP_PORT: Optional[int]
    SMTP_HOST: Optional[str]
    SMTP_USER: Optional[str]
    SMTP_PASSWORD: Optional[str]

    FIRST_SUPERUSER: str = ""
    FIRST_SUPERUSER_PASSWORD: str = ""

    MONGO_USER: str
    MONGO_PASS: str
    MONGO_HOST: str
    MONGO_DB: str = "epromo"

    SPACES_KEY: str
    SPACES_SECRET: str
    SPACES_URL: str

    CDN_URL: str


settings = Settings()
