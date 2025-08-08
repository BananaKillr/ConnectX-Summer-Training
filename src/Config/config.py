from pydantic_settings import BaseSettings
from typing import List,Dict

class Settings(BaseSettings):


    # ============================ Vector DB Configs =========================================
    Qdrant_db_path:str
    Qdrant_distance_method:str
    GOOGLE_API_KEY: str
    EMBEDDING_MODEL_NAME: str
    TEXT_EMBEDDING_MODEL_SIZE: str


    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()