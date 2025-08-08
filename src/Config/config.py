from pydantic_settings import BaseSettings
from typing import List,Dict

class Settings(BaseSettings):


    # ============================ Vector DB Configs =========================================
    Qdrant_db_path:str
    Qdrant_distance_method:str


    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()