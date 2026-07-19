import os
import re
from urllib.parse import quote
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import Config
from utils import parse_pdf_structured, optimize_for_tokens


def run_indexing(vector_store):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        add_start_index=True
    )

    folder_path = str(Config.DATA_DIR)

    all_chunks = []

    # Парсим
    for item in os.listdir(folder_path):
        if item.endswith('.pdf'):
            full_path = os.path.join(folder_path, item)

            print(f"Обработка: {item}")

            # 1. Парсим PDF
            text = parse_pdf_structured(full_path)

            # 2. Оптимизируем для токенов
            optimized_text = optimize_for_tokens(text)


            src = f'https://3.shkolkovo.online/st/6/o/{quote(item)}'

            # Делим текст на чанки
            chunk = text_splitter.create_documents(
                [optimized_text],
                metadatas=[{'source': src, "file": item}]
            )

            all_chunks.extend(chunk)

    # Добавляем в базу
    if all_chunks:
        vector_store.add_documents(all_chunks)
