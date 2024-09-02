from config import OPENAI_API_KEY
import os
import json
import logging
import openai
import docx2txt


# Устанавливаем API ключ
openai.api_key = OPENAI_API_KEY
# Создание клиента OpenAI
try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logging.error(f"Ошибка при создании клиента OpenAI: {str(e)}")
    client = None

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Базовый путь к папке с документами
BASE_PATH = "Для всех"


def get_text_from_docx(docx_path):
    try:
        text = docx2txt.process(docx_path)
        logging.info(f"Извлеченный текст из файла {docx_path}: '{text[:100]}'")
        return text.strip() if text else None
    except Exception as e:
        logging.error(f"Ошибка при чтении файла {docx_path}: {str(e)}")
        return None


def send_prompt_to_gpt(prompt, user_text):
    try:
        logging.info(f"Отправка запроса к ChatGPT")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_text}
            ]
        )
        summary = response.choices[0].message.content.strip()
        logging.info(f"Ответ от ChatGPT: {summary}")
        return summary
    except Exception as e:
        logging.error(f"Ошибка при отправке запроса в OpenAI: {str(e)}")
        return None


def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        contents = {}
        for file in files:
            if file.endswith(".docx"):
                file_path = os.path.join(root, file)
                text = get_text_from_docx(file_path)
                if text:
                    prompt = "Проанализируй этот текст и напиши краткое содержание. Отвечай только самим кратким содержанием и ничем больше."
                    summary = send_prompt_to_gpt(prompt, text)
                    if summary:
                        contents[file] = summary
                    else:
                        logging.error(f"Ошибка при получении ответа от ChatGPT для файла {file_path}")

        if contents:
            output_file_path = os.path.join(root, "Содержание.json")
            try:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    json.dump(contents, f, ensure_ascii=False, indent=4)
                logging.info(f"Создан файл {output_file_path}")
            except Exception as e:
                logging.error(f"Ошибка при сохранении файла {output_file_path}: {str(e)}")


if __name__ == "__main__":
    try:
        process_directory(BASE_PATH)
    except Exception as e:
        logging.error(f"Ошибка в процессе выполнения: {str(e)}")
