from pydantic_settings import BaseSettings


class Settings:
    MODEL_NAME: str = "homebrewltd/Ichigo-llama3.1-s-instruct-v0.4"
    VECTORDB_PATH: str = "temp_vectordb"
    WHISPER_MODEL: str = "base"


settings = Settings()
