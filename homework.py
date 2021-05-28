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
HOMEWORK_STATUSES = {
    'reviewing': 'Работа взята в ревью.',
    'approved': (
        'Ревьюеру всё понравилось, '
        'можно приступать к следующему уроку.'
    ),
    'rejected': 'К сожалению в работе нашлись ошибки.',
}


def parse_homework_status(homework):
    """
    Возвращает статус домашней работы.
    homework - словарь с информацией о домашней работе.
    """
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None or homework_status is None:
        logging.error(
            f'Не удалось получить имя или статус дз! Ошибка: {TypeError}'
        )
        raise TypeError
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    """
    Отправляет запрос об изменении статусов домашней работы.
    current_timestamp - метка времени с которой выбираются сообщения.
    """
    if current_timestamp is None:
        current_timestamp = int(time.time())
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
    except requests.exceptions.RequestException as e:
        logging.error(
            f'Не удалось получить статус дз! Ошибка: {e}'
        )
        raise requests.exceptions.RequestException


def send_message(message, bot_client):
    """
    Отправляет сообщение в телеграм.
    message - текст отправляемого сообщения.
    bot_client - клиент для отправки сообщения.
    """
    try:
        return bot_client.send_message(chat_id=CHAT_ID, text=message)
        logging.info(f'Сообщение отправлено! Текст: {message}')
    except telegram.error.TelegramError as e:
        logging.error(
            f'Не удалось отправить сообщение! Ошибка: {e}'
        )
        raise telegram.error.TelegramError


def main():
    """
    Опрашивает на наличие обновлений Яндекс.Практикум,
    в случае появления нового статуса,
    бот отсылает сообщение в телеграм.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        filename='homework.log',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    bot_client = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    logging.info('Успешный запуск бота!')
    send_message('Бот запущен!', bot_client)
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                logging.info(
                    'Успешная проверка обновлений! '
                    f'{new_homework.get("homeworks")[0]}'
                )
                send_message(parse_homework_status(
                    new_homework.get('homeworks')[0]), bot_client
                )
            current_timestamp = new_homework.get(
                'current_date', current_timestamp
            )
            time.sleep(300)

        except Exception as e:
            logging.error(f'Бот столкнулся с ошибкой: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
