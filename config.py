from pydantic import BaseSettings

class Config(BaseSettings):
    elastic_user: str
    elastic_password: str
    elastic_cloud_id: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

config = Config()  # type: ignore
