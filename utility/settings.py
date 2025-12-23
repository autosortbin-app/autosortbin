from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ThingSpeak
    thingspeak_channel_id: int = Field(..., env="THINGSPEAK_CHANNEL_ID")
    thingspeak_write_api_key: str = Field(..., env="THINGSPEAK_WRITE_API_KEY")
    thingspeak_read_api_key: str = Field(..., env="THINGSPEAK_READ_API_KEY")

    # Email (Brevo)
    brevo_api_key: str = Field(..., env="BREVO_API_KEY")
    email_sender: str = Field(..., env="EMAIL_SENDER")
    email_admin: str = Field(..., env="EMAIL_ADMIN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
