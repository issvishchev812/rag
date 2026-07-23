import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    # API
    PROXY_API_KEY = os.environ.get('PROXY_API_KEY')
    BASE_URL = "https://api.proxyapi.ru/openai/v1"
    API_TG = os.environ.get('API_TG')

    # Модели
    EMBED_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o-mini"
    TEMPERATURE = 0.1

    # RAG параметры
    CHUNK_SIZE = 700
    CHUNK_OVERLAP = 100
    RETRIEVER_K = 5

    # Пути
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    DB_DIR = BASE_DIR / "chroma_db"
