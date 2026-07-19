import re

import fitz


def parse_pdf_structured(file_path):
    try:
        with fitz.open(file_path) as doc:

            structured_text = []

            for page_num, page in enumerate(doc, 1):
                # Получаем блоки текста
                blocks = page.get_text("blocks")

                page_blocks = []
                for block in blocks:
                    text = block[4].strip()
                    if text:
                        page_blocks.append(text)

                # Объединяем блоки с разделением по абзацам
                if page_blocks:
                    structured_text.append('\n\n'.join(page_blocks))

            full_text = '\n\n--- НОВАЯ СТРАНИЦА ---\n\n'.join(structured_text)

            return full_text

    except Exception as e:
        print(f"Ошибка при парсинге PDF {file_path}: {e}")
        return ""



def optimize_for_tokens(text):
    """Оптимизирует текст для экономии токенов"""

    if not text:
        return ""

    # 1. Убираем служебную информацию
    text = re.sub(r'--- НОВАЯ СТРАНИЦА ---', '', text)
    text = re.sub(r'© 2026.*?науки', '', text)
    text = re.sub(r'Спецификация КИМ ЕГЭ \d{4} г\..*?\d+ / \d+', '', text)
    text = re.sub(r'РУССКИЙ ЯЗЫК, \d+ класс\.\s*\d+ / \d+', '', text)

    # 2. Нормализуем пустые строки
    text = re.sub(r'\n{3,}', '\n\n', text)

    # 3. Убираем пустые строки в начале и конце
    text = text.strip()

    # 4. Убираем пробелы в конце строк
    text = '\n'.join(line.rstrip() for line in text.split('\n'))

    # 5. Убираем строки с одним пробелом или пустые
    lines = [line for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)

    return text


def format_docs(docs):
    """Форматирует документы для контекста"""
    formatted = []
    for doc in docs:
        source = doc.metadata.get('source', 'неизвестен')
        content = doc.page_content
        formatted.append(f"Текст:{content}\n Ссылка: {source}")
    return  "\n\n" .join(formatted)