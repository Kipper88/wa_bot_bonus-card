import asyncio
from flask import Flask, request
import time

from handlers import handle_message
from states import StateUser

import logging

logging.basicConfig(
    filename='example.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
    
app = Flask(__name__)

@app.route('/', methods=['POST'])
async def webhook():
    data = request.json

    try:
        if data['messageData']['typeMessage'] == 'textMessage':
            chat_id = data['senderData']['chatId'].split('@')[0]
            text = data['messageData']['textMessageData']['textMessage']
            await handle_message(chat_id, text)
            logging.info(f'Сообщение от {chat_id} успешно обработано')           
        return "OK", 200
    except Exception:
        logging.error(f"Произошла ошибка при обработке сообщения от юзера {data['senderData']['chatId'].split('@')[0]}")

async def checker_state():
    while True:
        for i in StateUser.birthday:
            if StateUser.birthday[i] < time.time - 1800: # 30 мин
                del StateUser.birthday[i]
                logging.indo(f'Удалено ожидание ввода даты рождения от юзера {i}')
            await asyncio.sleep(60)

if __name__ == '__main__':
    logging.info(f'Запуск сервера под именем {__name__}.')
    loop = asyncio.get_event_loop()
    loop.create_task(checker_state())
    app.run(port=9224)
    logging.info(f'Сервер под именем {__name__} успешно запущен')
