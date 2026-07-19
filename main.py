from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from utils import format_docs
from indexer import run_indexing
from config import Config


load_dotenv()

PROXY_API_KEY = Config.PROXY_API_KEY


embeddings = OpenAIEmbeddings(
    openai_api_key=PROXY_API_KEY,
    model=Config.EMBED_MODEL,
    base_url=Config.BASE_URL
)


llm = ChatOpenAI(
    openai_api_key=PROXY_API_KEY,
    model=Config.LLM_MODEL,
    temperature=0.1,
    base_url=Config.BASE_URL
)

# Инициализируем векторную БД
vector_store = Chroma(
    collection_name="ege_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

try:
    collection_size = vector_store._collection.count()
    if collection_size == 0:
        print('База данных пуста. Инициализация...')
        run_indexing(vector_store)
except Exception as e:
    print(f"Ошибка при проверке базы данных: {e}")
    try:
        print('Инициализация...')
        run_indexing(vector_store)
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")


# Ретривер
retriever = vector_store.as_retriever(
    search_kwargs={"k": Config.RETRIEVER_K}
)

# Промпт
prompt_template = """
Ты — эксперт по русскому языку, который помогает готовиться к ЕГЭ.
Твоя задача — найти в предоставленном контексте информацию, которая отвечает на вопрос пользователя, и сформулировать чёткий, структурированный ответ.

ИНСТРУКЦИЯ:
1. Внимательно прочитай ВЕСЬ предоставленный контекст.
2. Найди в нём ВСЮ информацию, которая относится к вопросу.
3. Если вопрос просит перечислить что-то — перечисли ВСЕ найденные примеры, не пропуская ни одного.
4. Структурируй ответ: группируй информацию по типам, используй списки.
5. ЕСЛИ В КОНТЕКСТЕ НЕТ НУЖНОЙ ИНФОРМАЦИИ — ответь ЧЕСТНО: "В предоставленных материалах нет ответа на этот вопрос."
6. ОБЯЗАТЕЛЬНО добавь в конце ответа источник информации (ссылку из метаданных).

Контекст:
{context}

Вопрос пользователя:
{query}

Твой ответ:
"""

prompt = PromptTemplate.from_template(prompt_template)

# RAG-цепочка
rag_chain = (
    {"context": retriever | format_docs, "query": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

if __name__ == '__main__':
    try:
        response = rag_chain.invoke("Какие корни с чередованием гласных бывают в русском языке?")
        print(response)
    except Exception as e:
        print(f'Ошибка при исполнении запроса:\n {e}')
