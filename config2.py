# TELEGRAM_API_TOKEN = '7460711585:AAHJq-4U8eYXzPGyy-krCB6ayDeuwa9tNWk'
OPENAI_API_KEY = 'sk-proj-f5rM50RBLLXNWs9xzF7tT3BlbkFJhsNV7V9HfOmy4Pe9n4pb'
TELEGRAM_API_TOKEN = '6525958909:AAFPcotiysHE6YG9nuo0-QPTSKOZNtew0ms'

# PROMPT = ('На протяжении всего чата ты должен строго следовать предоставленной информации и ни в коем случае не '
#           'добавлять ничего от себя. Я буду предоставлять тебе определенные данные, и ты можешь использовать для '
#           'ответа только эти данные. Анализируй всю информацию, которую я тебе дам. На мои вопросы отвечай '
#           'исключительно на основе предоставленных данных. Если в информации нет ответа на мой запрос, '
#           'отвечай: "Извините, я могу помочь только с предоставленными документами/Информация по запросу не найдена". '
#           'Мои вопросы могут не совпадать дословно с текстом, который я дам, но ты обязан найти наиболее подходящую по '
#           'смыслу информацию и использовать её в ответе. Обязательно указывай ссылку или название документа, '
#           'из которого берется информация. Никаких собственных интерпретаций или добавлений! Отвечай только на основе '
#           'предоставленных данных или сообщай: "Извините, я могу помочь только с предоставленными '
#           'документами/Информация по запросу не найдена". Также, если мне потребуется уточнение по вопросу или '
#           'дополнительная информация, ты можешь отвечать на основе предоставленных ранее данных.')


PROMPT =('На протяжении всего чата ты должен строго следовать предоставленной информации и ни в коем случае не '
         'добавлять ничего от себя. Я буду предоставлять тебе определенные данные, и ты можешь использовать для '
         'ответа только эти данные. Анализируй всю информацию, которую я тебе дам. На мои вопросы отвечай '
         'исключительно на основе предоставленных данных. Если в информации нет ответа на мой запрос, '
         'отвечай: "Извините, я могу помочь только с предоставленными документами/Информация по запросу не найдена". '
         'Мои вопросы могут не совпадать дословно с текстом, который я дам, но ты обязан найти наиболее подходящую по '
         'смыслу информацию и использовать её в ответе. Обязательно указывай ссылку или название документа, '
         'из которого берется информация. Никаких собственных интерпретаций или добавлений! Отвечай только на основе '
         'предоставленных данных или сообщай: "Извините, я могу помочь только с предоставленными '
         'документами/Информация по запросу не найдена".')

# PROMPT = ('НА ПРОТЯЖЕНИИ ВСЕГО ЧАТА НИ В КОЕМ СЛУЧАЕ НЕ ПИШИ НИЧЕГО ОТ СЕБЯ!!! Я предоставлю тебе определённую '
#           'информацию, и ты можешь использовать для ответа только её. Проанализируй всю информацию, которую я тебе '
#           'дам. На мои вопросы отвечай, опираясь исключительно на предоставленные данные. Если в информации нет '
#           'ответа на мой запрос, отвечай: "Извините, я могу помочь только с предоставленными документами/Информация '
#           'по запросу не найдена". Мои вопросы могут не совпадать дословно с текстом, который я дам, но ты должен '
#           'найти наиболее подходящую по смыслу информацию и использовать её в ответе. Дай ссылку/сноску на документ '
#           'или название документа, информацию из которого ты предоставляешь. НИ В КОЕМ СЛУЧАЕ НЕ ПИШИ НИЧЕГО ОТ СЕБЯ! '
#           'Отвечай только на основе предоставленных данных либо "Извините, я могу помочь только с предоставленными '
#           'документами/Информация по запросу не найдена".!!!')


# PROMPT_START = ('Для каждого запроса отвечай исключительно по существу и предельно кратко. Если вопрос предполагает '
#                 'получение информации из файла, ответ должен содержать только ответ на вопрос на основе данных из '
#                 'файла, без дополнительных пояснений или комментариев. Если запрос требует названия файла, '
#                 'укажи только его название. Любая отсебятина, комментарии или дополнения запрещены.')

PROMPT_START = ('Отвечай на каждый запрос исключительно по существу и максимально кратко. Если вопрос требует '
                'информацию из файла, ответ должен содержать только конкретные данные из файла, без дополнительных '
                'пояснений или комментариев. Если запрос предполагает указание названия файла, укажи только его '
                'название. Любая отсебятина, комментарии или дополнения строго запрещены.')

# PROMPT_GET_FILE_NAME = ('Проанализируй следующий запрос от пользователя и выбери максимум 3 названия файлов из '
#                         'предоставленных в JSON, которые наиболее вероятно содержат информацию, соответствующую '
#                         'запросу. В ответе в "" и через запятую укажи только название файлов, никаких дополнительных '
#                         'комментариев или пояснений. JSON: ')

PROMPT_GET_FILE_NAME = ('Проанализируй следующий запрос от пользователя и выбери до 3 названий файлов из '
                        'предоставленных в JSON, которые наиболее вероятно содержат информацию, соответствующую '
                        'запросу. В ответе укажи только названия файлов в кавычках и через запятую, '
                        'без дополнительных комментариев или пояснений. JSON: ')

# PROMPT_GIVE_ANSWER = ('Вот текст файлов и запрос пользователя. Проанализируй текст и дай полную цитату, отвечающую на '
#                       'запрос пользователя, опираясь только на информацию, содержащуюся в тексте предоставленном '
#                       'ранее. В ответе укажи только конкретный ответ на запрос, без дополнительных комментариев или '
#                       'пояснений. На запросы не связанные с информацией полученной ранее отвечай "Запрос не относится '
#                       'к документам". Запрос пользователя: ')

PROMPT_GIVE_ANSWER = ('Вот текст файлов и запрос пользователя. Проанализируй текст и предоставь точную цитату, '
                      'которая полностью отвечает на запрос пользователя, опираясь только на информацию из '
                      'предоставленного текста. Ответ должен содержать исключительно необходимую информацию, '
                      'без дополнительных комментариев или пояснений. Если запрос не связан с предоставленными '
                      'данными, отвечай: "Запрос не относится к документам". Запрос пользователя: ')

# PROMPT_CHECK_CONTINUITY = ('Определи, является ли следующий запрос пользователя уточнением, продолжением или '
#                            'дополнительным вопросом по теме, обсуждаемой ранее в текущей сессии. Если запрос связан, '
#                            'ответь "Да", если нет, ответь "Нет". Запрос пользователя: ')

# PROMPT_CHECK_CONTINUITY = ('Определи, связан ли следующий запрос пользователя с темой, обсуждаемой ранее в текущей сессии. '
#                            'Если запрос является уточнением, продолжением или дополнительным вопросом по текущей теме, '
#                            'ответь "Да". Если запрос не связан с предыдущим обсуждением, ответь "Нет". '
#                            'Запрос пользователя: ')


PROMPT_CHECK_CONTINUITY = ('Определи, связан ли следующий запрос пользователя с темой, обсуждаемой ранее в текущей сессии. '
                           'Если запрос является уточнением, продолжением, просьбой о расширении или дополнительным вопросом '
                           'по текущей теме, ответь "Да". Включай в "Да" также запросы на получение дополнительной информации '
                           'или разъяснений по ранее данному ответу. Если запрос не связан с предыдущим обсуждением, ответь "Нет". '
                           'Запрос пользователя: ')


COMPANIES = [
    "Биг-Беги",
    "Европа",
    "Известняк",
    "УК"
]

POSITIONS = [
    "ГД", "ИД", "РО1", "РО2", "РО3", "РО4", "РО5", "РО6", "НО2",
    "НО7", "НО8", "НО9", "НО10", "НО11", "НО12", "НО14"
]