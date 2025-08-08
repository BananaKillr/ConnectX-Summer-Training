import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from Database.vectordb.Qdrant import Qdrant
from LLMs.Embedding import e5Model
from LLMs.Gemini import GEMINI
from Config.config import get_settings
from Routes.data import data_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    settings = get_settings()
    app.db_client = Qdrant(db_path=settings.Qdrant_db_path,distance_method=settings.Qdrant_distance_method).connect()
    app.embedding_client = e5Model(model_name=settings.EMBEDDING_MODEL_NAME)
    app.llm = GEMINI(model_name=settings.GEMINI_MODEL_NAME)
    
    yield
    
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_router)
