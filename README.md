# «Telegram-бот»
## Описание
Телеграм-бот обращается к API Практикума и узнаёт статус вашего домашнего задания (работа взята в ревью, ревьюеру всё понравилось, в работе нашлись ошибки). Полученный статус дз отправляется в ваш Телеграм.

## Установка
Для работы бота потребуется файл .env со следующим перечнем переменных:
- PRAKTIKUM_TOKEN=YOUR_PRACTICUM_TOKEN # Токен Яндекс.Практикум
- TELEGRAM_TOKEN=YOUR_TELEGRAM_TOKEN # Токен вашего бота
- TELEGRAM_CHAT_ID=YOUR_TELEGRAM_CHAT_ID # Ваш Chat_id

Клонируем репозиторий на локальную машину:

`git clone https://github.com/DenisSivko/api_sp1_bot.git`

Создаем виртуальное окружение:

`python -m venv venv`

Устанавливаем зависимости:

`pip install -r requirements.txt`

Запуск:

`python homework.py`
