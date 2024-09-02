import json
from config import TELEGRAM_API_TOKEN, OPENAI_API_KEY, COMPANIES, POSITIONS, PROMPT_START, PROMPT_GET_FILE_NAME, \
    PROMPT_GIVE_ANSWER, PROMPT_CHECK_CONTINUITY
import openai
import telebot
from telebot import types
import os
import logging
import re
import docx2txt


send_once_flag = False

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_API_TOKEN)

# Создание клиента OpenAI
try:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
except Exception as e:
    logging.error(f"Ошибка при создании клиента OpenAI: {str(e)}")
    client = None

# Словарь для хранения данных пользователя
user_data = {}

# Базовый путь к папке с документами
# BASE_PATH = "input"
BASE_PATH = "input2"
# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        user_data.pop(message.chat.id, None)  # Сброс состояния пользователя при старте
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for company in COMPANIES:
            markup.add(types.KeyboardButton(company))
        markup.add(types.KeyboardButton("Перезапустить бот"))
        bot.send_message(message.chat.id, "Выберите компанию:", reply_markup=markup)
    except Exception as e:
        logging.error(f"Ошибка в обработке команды /start: {str(e)}")


# Обработка кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back(message):
    try:
        logging.info(f"Пользователь {message.chat.id} нажал 'Назад'")
        if user_data.get(message.chat.id, {}).get("chat_active", False):
            user_data[message.chat.id].pop("chat_active", None)
            global chat_histories
            chat_histories = {}
            show_chat_options(message)
        elif user_data.get(message.chat.id, {}).get("position"):
            show_positions_menu(message)
        elif user_data.get(message.chat.id, {}).get("company"):
            start(message)
        else:
            start(message)
    except Exception as e:
        logging.error(f"Ошибка в обработке кнопки 'Назад': {str(e)}")


# Обработка кнопки "Перезапустить бот"
@bot.message_handler(func=lambda message: message.text == "Перезапустить бот")
def handle_restart(message):
    try:
        logging.info(f"Пользователь {message.chat.id} перезапустил бота")
        global chat_histories
        chat_histories = {}
        start(message)
    except Exception as e:
        logging.error(f"Ошибка в обработке кнопки 'Перезапустить бот': {str(e)}")


# Обработка выбора компании
@bot.message_handler(func=lambda message: message.text in COMPANIES)
def handle_company_choice(message):
    try:
        logging.info(f"Пользователь {message.chat.id} выбрал компанию: {message.text}")
        user_data[message.chat.id] = {"company": message.text}
        bot.send_message(message.chat.id, f"Вы выбрали: {message.text}")
        show_positions_menu(message)
    except Exception as e:
        logging.error(f"Ошибка в обработке выбора компании: {str(e)}")


# Показать меню с должностями
def show_positions_menu(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for position in POSITIONS:
            markup.add(types.KeyboardButton(position))
        markup.add(types.KeyboardButton("Назад"), types.KeyboardButton("Перезапустить бот"))
        bot.send_message(message.chat.id, "Выберите должность:", reply_markup=markup)
    except Exception as e:
        logging.error(f"Ошибка в показе меню должностей: {str(e)}")


def load_file_content(file_path):
    try:
        if file_path.endswith('.docx'):
            text = docx2txt.process(file_path)
            logging.info(f"Извлеченный текст из файла {file_path}: '{text[:100]}'")
            return text.strip() if text else None
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read().strip()
                logging.info(f"Извлеченное содержимое файла {file_path}: '{content[:100]}'")
                return content if content else None
    except FileNotFoundError:
        logging.error(f"Файл не найден: {file_path}")
    except Exception as e:
        logging.error(f"Ошибка при загрузке файла {file_path}: {str(e)}")
    return None


def load_documents(company, position, file_names):
    combined_text = []

    for file_name in file_names:
        try:
            # Пути к файлам
            file_path = os.path.join(BASE_PATH, company, position, file_name)
            file_path_for_all = os.path.join(BASE_PATH, company, "Для всех", file_name)

            # Логирование путей к файлам
            logging.info(f"Проверка файлов: {file_path} и {file_path_for_all}")

            # Проверка и загрузка файла для конкретной должности
            if os.path.isfile(file_path):
                file_content = load_file_content(file_path)
                if file_content:
                    combined_text.append(file_content)
                else:
                    logging.warning(f"Файл не был загружен: {file_path}")

            # Проверка и загрузка общего файла для компании
            elif os.path.isfile(file_path_for_all):
                file_content = load_file_content(file_path_for_all)
                if file_content:
                    combined_text.append(file_content)
                else:
                    logging.warning(f"Файл не был загружен: {file_path_for_all}")
        except Exception as e:
            logging.error(f"Ошибка при обработке файла {file_name} для компании {company} и должности {position}: {str(e)}")

    logging.info(combined_text)
    return '\n\n'.join(combined_text) if combined_text else None


def load_json_content(company, position):
    file_path = os.path.join(BASE_PATH, company, position, "Содержание.json")
    file_path_for_all = os.path.join(BASE_PATH, company, "Для всех", "Содержание.json")

    logging.info(f"Путь к файлу {file_path_for_all}")
    combined_content = []

    try:
        # Загрузка общего файла для компании
        with open(file_path_for_all, 'r', encoding='utf-8') as file:
            json_content_for_all = json.load(file)
            if isinstance(json_content_for_all, list):
                combined_content.extend(json_content_for_all)
            elif isinstance(json_content_for_all, dict):
                combined_content.append(json_content_for_all)
    except FileNotFoundError:
        logging.error(f"Файл не найден: {file_path_for_all}")
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON файла {file_path_for_all}: {str(e)}")
    except Exception as e:
        logging.error(f"Ошибка загрузки общего JSON файла для компании: {str(e)}")

    try:
        # Загрузка файла для конкретной должности
        with open(file_path, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
            if isinstance(json_content, list):
                combined_content.extend(json_content)
            elif isinstance(json_content, dict):
                combined_content.append(json_content)
    except FileNotFoundError:
        logging.error(f"Файл не найден: {file_path}")
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка декодирования JSON файла {file_path}: {str(e)}")
    except Exception as e:
        logging.error(f"Ошибка загрузки JSON файла для должности: {str(e)}")

    if combined_content:
        return json.dumps(combined_content, ensure_ascii=False, indent=2)
    else:
        return None


chat_histories = {}


def send_prompt(bot, chat_id, combined_prompt, user_text):
    try:
        logging.info(f"Отправка документа целиком для пользователя {chat_id}")

        # Проверка, есть ли уже история сообщений для данного чата
        if chat_id not in chat_histories:
            # Если истории нет, создаем её и добавляем системное сообщение
            chat_histories[chat_id] = [{"role": "system", "content": combined_prompt}]

        # Добавление нового сообщения пользователя в историю
        chat_histories[chat_id].append({"role": "user", "content": user_text})

        if client is None:
            bot.send_message(chat_id, "Ошибка при создании клиента OpenAI, попробуйте позже.")
            return

        # Отправка запроса к ChatGPT с учетом всей истории диалога
        logging.info(f"Отправка запроса к ChatGPT для пользователя {chat_id}")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=chat_histories[chat_id]
        )

        # Сбор ответа
        answer = response.choices[0].message.content.strip()

        logging.info(f"Ответ от ChatGPT: {answer}")

        # Добавление ответа модели в историю
        chat_histories[chat_id].append({"role": "assistant", "content": answer})

        return answer
    except Exception as e:
        logging.error(f"Ошибка при отправке запроса в OpenAI: {str(e)}")
        bot.send_message(chat_id, "Произошла ошибка при отправке запроса, попробуйте позже.")
        return None


def send_long_message(bot, chat_id, text):
    try:
        max_length = 4096
        for i in range(0, len(text), max_length):
            bot.send_message(chat_id, text[i:i + max_length])
    except Exception as e:
        logging.error(f"Ошибка при отправке длинного сообщения: {str(e)}")


@bot.message_handler(func=lambda message: message.text in POSITIONS)
def handle_position_choice(message):
    try:
        logging.info(f"Пользователь {message.chat.id} выбрал должность: {message.text}")
        user_data[message.chat.id]["position"] = message.text
        bot.send_message(message.chat.id, f"Вы выбрали должность: {message.text}")
        show_chat_options(message)
    except Exception as e:
        logging.error(f"Ошибка в обработке выбора должности: {str(e)}")


def show_chat_options(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Новая тема"))
        markup.add(types.KeyboardButton("Назад"), types.KeyboardButton("Перезапустить бот"))
        bot.send_message(message.chat.id, "Что вы хотите сделать дальше?", reply_markup=markup)
    except Exception as e:
        logging.error(f"Ошибка в показе опций чата: {str(e)}")


@bot.message_handler(func=lambda message: message.text == "Новая тема")
def handle_new_chat(message):
    try:
        logging.info(f"Пользователь {message.chat.id} начал новую тему")
        company = user_data[message.chat.id]["company"]
        position = user_data[message.chat.id]["position"]
        combined_prompt = f"{PROMPT_START}" + ' Я сотрудник компании ' + company + ' с должностью ' + position
        user_data[message.chat.id]["chat_active"] = True
        user_data[message.chat.id]["combined_prompt"] = combined_prompt
        send_prompt(bot, message.chat.id, combined_prompt, combined_prompt)
        send_long_message(bot, message.chat.id, "Готов к обработке запроса")

    except Exception as e:
        logging.error(f"Ошибка в обработке новой темы: {str(e)}")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("chat_active", False))
def handle_user_message(message):
    try:
        logging.info(f"Пользователь {message.chat.id} задал вопрос в активной сессии")

        if "combined_prompt" not in user_data[message.chat.id]:
            bot.send_message(message.chat.id,
                             "Произошла ошибка: контекст не был установлен. Пожалуйста, начните заново.")
            return

        # Получаем текущий запрос пользователя
        user_text = message.text
        combined_prompt = user_data[message.chat.id]["combined_prompt"]


        # Шаг 1: Проверка, связан ли текущий запрос с предыдущими
        continuity_check_prompt = f"{PROMPT_CHECK_CONTINUITY} {user_text}"
        continuity_check_response = send_prompt(bot, message.chat.id, combined_prompt, continuity_check_prompt)
        logging.info(f"Отправленно: {continuity_check_prompt}")
        logging.info(f"Промпт: {user_text}")
        logging.info(f"Результат проверки связи запроса: {continuity_check_response}")

        global send_once_flag

        if re.search(r'\bда\b', continuity_check_response.strip(), re.IGNORECASE) and send_once_flag:
            # Если запрос связан, обрабатываем без загрузки файлов
            collected_answers = send_prompt(bot, message.chat.id, combined_prompt, "Основываясь на ранее обработанных и отправленных запросах" + user_text )
            logging.info(f"Ответ от ChatGPT без загрузки файлов: {collected_answers}")
            send_long_message(bot, message.chat.id, collected_answers)
        else:
            send_once_flag = True
            # Шаг 2: Обработка запроса по стандартной логике с загрузкой файлов
            company = user_data[message.chat.id]["company"]
            position = user_data[message.chat.id]["position"]

            json_info = load_json_content(company, position)

            if json_info:
                user_text = PROMPT_GET_FILE_NAME + json_info + "\nЗапрос пользователя:\n" + user_text

                logging.info(f"К ChatGPT выслан запрос: {user_text}")

                collected_answers = send_prompt(bot, message.chat.id, combined_prompt, user_text)

                logging.info(f"От ChatGPT получен ответ: {collected_answers}")
                bot.send_message(message.chat.id, "Ответ может находиться в файлах: ")
                send_long_message(bot, message.chat.id, collected_answers)

                bot.send_message(message.chat.id, "Обрабатываю ответ...")

                # Преобразуем ответ от ChatGPT в список файлов, разделяя по кавычкам
                file_list = re.findall(r'"(.*?)"', collected_answers)

                if len(file_list) < 1:
                    file_list = [collected_answers]

                logging.info(f"Список файлов для загрузки: {file_list}")

                document = load_documents(company, position, file_list)

                logging.info(f"Загруженные документы: {document}")

                if document:
                    user_text = PROMPT_GIVE_ANSWER + 'Запрос пользователя: Я сотрудник компании ' + company + ' с должностью ' + position + ' ' + message.text + ' Текст файла: ' + document

                    logging.info(f"К ChatGPT выслан запрос: {user_text}")

                    collected_answers = send_prompt(bot, message.chat.id, combined_prompt, user_text)

                    logging.info(f"От ChatGPT получен ответ: {collected_answers}")
                    send_long_message(bot, message.chat.id, collected_answers)
                else:
                    bot.send_message(message.chat.id, "Ошибка в загрузке документа, попробуйте повторить запрос")
            else:
                bot.send_message(message.chat.id, "Ошибка в загрузке списка документов, попробуйте повторить запрос")
    except Exception as e:
        logging.error(f"Ошибка в обработке сообщения пользователя: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса, попробуйте снова.")


# Запуск бота
if __name__ == '__main__':
    send_once_flag = False
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Ошибка в работе бота: {str(e)}")


# def send_prompt(bot, chat_id, combined_prompt, user_text):
#     try:
#         logging.info(f"Отправка документа целиком для пользователя {chat_id}")
#
#         messages = [
#             {"role": "system", "content": combined_prompt},
#             {"role": "user", "content": user_text}
#         ]
#
#         if client is None:
#             bot.send_message(chat_id, "Ошибка при создании клиента OpenAI, попробуйте позже.")
#             return
#
#         # Отправка запроса к ChatGPT
#         logging.info(f"Отправка запроса к ChatGPT для пользователя {chat_id}")
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages
#         )
#
#         # Сбор ответа
#         answer = response.choices[0].message.content.strip()
#
#         logging.info(f"Ответ от ChatGPT: {answer}")
#
#         return answer
#     except Exception as e:
#         logging.error(f"Ошибка при отправке запроса в OpenAI: {str(e)}")
#         bot.send_message(chat_id, "Произошла ошибка при отправке запроса, попробуйте позже.")
#         return None


# Словарь для хранения истории сообщений для каждого чата


# @bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("chat_active", False))
# def handle_user_message(message):
#     try:
#         logging.info(f"Пользователь {message.chat.id} задал вопрос в активной сессии")
#         if "combined_prompt" not in user_data[message.chat.id]:
#             bot.send_message(message.chat.id, "Произошла ошибка: контекст не был установлен. Пожалуйста, начните "
#                                               "заново.")
#             return
#
#         company = user_data[message.chat.id]["company"]
#         position = user_data[message.chat.id]["position"]
#
#         json_info = load_json_content(company, position)
#
#         if json_info:
#             user_text = PROMPT_GET_FILE_NAME + json_info + ' Я сотрудник компании ' + company + ' с должностью ' + position + ' ' + message.text + ' '
#
#             logging.info(f"К ChatGPT выслан запрос: {user_text}")
#
#             combined_prompt = user_data[message.chat.id]["combined_prompt"]
#
#             # Отправка документа частями и сбор ответов
#             collected_answers = send_prompt(bot, message.chat.id, combined_prompt, user_text)
#
#             logging.info(f"От ChatGPT получен ответ: {collected_answers}")
#             bot.send_message(message.chat.id, "Ответ может находиться в файлах: ")
#             send_long_message(bot, message.chat.id, collected_answers)
#
#             bot.send_message(message.chat.id, "Обрабатываю ответ...")
#
#             # Преобразуем ответ от ChatGPT в список файлов, разделяя по кавычкам
#             file_list = re.findall(r'"(.*?)"', collected_answers)
#
#             if len(file_list) < 1:
#                 file_list = [collected_answers]
#
#             logging.info(f"Список файлов для загрузки: {file_list}")
#
#             document = load_documents(company, position, file_list)
#
#             logging.info(f"Загруженные документы: {document}")
#
#             if document:
#                 user_text = PROMPT_GIVE_ANSWER + 'Запрос пользователя: Я сотрудник компании' + company + 'с должностью' + position + message.text + 'Текст файла:' + document
#
#                 logging.info(f"К ChatGPT выслан запрос: {user_text}")
#
#                 collected_answers = send_prompt(bot, message.chat.id, combined_prompt, user_text)
#
#                 logging.info(f"От ChatGPT получен ответ: {collected_answers}")
#                 send_long_message(bot, message.chat.id, collected_answers)
#             else:
#                 bot.send_message(message.chat.id, "Ошибка в загрузке документа, попробуйте повторить запрос")
#         else:
#             bot.send_message(message.chat.id, "Ошибка в загрузке списка документов, попробуйте повторить запрос")
#     except Exception as e:
#         logging.error(f"Ошибка в обработке сообщения пользователя: {str(e)}")
#         bot.send_message(message.chat.id, "Произошла ошибка при обработке вашего запроса, попробуйте снова.")
