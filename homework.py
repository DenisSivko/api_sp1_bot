import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def parse_homework_status(homework):
    try:
        homework_name = homework.get('homework_name')
    except Exception as e:
        print(f'Не удалось получить имя дз! Ошибка: {e}')
        logging.error(e, exc_info=True)
    try:
        if homework['status'] == 'rejected':
            verdict = 'К сожалению в работе нашлись ошибки.'
        else:
            verdict = 'Ревьюеру всё понравилось, '\
                'можно приступать к следующему уроку.'
        return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'
    except Exception as e:
        print(f'Не удалось получить статус дз! Ошибка: {e}')
        logging.error(e, exc_info=True)


def get_homework_statuses(current_timestamp):
    data = {
        'from_date': current_timestamp,
        'token': PRAKTIKUM_TOKEN,
    }
    headers = {
        'Authorization': 'OAuth {}'.format(PRAKTIKUM_TOKEN)
    }
    try:
        homework_statuses = requests.get(
            'https://praktikum.yandex.ru/api/user_api/homework_statuses/',
            headers=headers, params=data)
        return homework_statuses.json()
    except Exception as e:
        print(f'Не удалось получить статус дз! Ошибка: {e}')
        logging.error(e, exc_info=True)


def send_message(message, bot_client):
    try:
        return bot_client.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f'Не удалось отправить сообщение! Ошибка: {e}')
        logging.error(e, exc_info=True)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        filename='homework.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]), bot_client
                )
            current_timestamp = new_homework.get(
                'current_date', current_timestamp
            )
            time.sleep(300)

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
