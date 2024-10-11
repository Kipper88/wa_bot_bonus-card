from database import Database

db = Database(name='default_db',
              user='gen_user',
              password='l,3Ty-TC;a^o\?',
              host='81.200.154.175'
              )
    
async def check_user(chat_id):
    return await db.query_select(f'SELECT "balance", "status", "stamp" FROM "user" WHERE "phone" = \'{str(chat_id)}\'')

async def insert_user(data):
    await db.query_insert('''INSERT INTO "user"(id, username, phone, balance, status, stamp, bday) VALUES($1, $2, $3, $4, $5, $6, $7)''',
                          data)
    
    
    
############################
############################
############################

from cfg import *
from aiohttp import ClientSession

# Функция для отправки сообщения
async def send_message(chat_id, message):
    url = BASE_URL + f'sendMessage/{apiTokenInstance}'
    payload = {
        "chatId": f"{chat_id}@c.us",  # формат для номера в WhatsApp
        "message": message
    }
    async with ClientSession() as session:
        response = await session.post(url, json=payload)
    return await response.json()

# Функция для отправки изображения
async def send_image(chat_id, caption, image_url):
    url = BASE_URL + f'sendFileByUrl/{apiTokenInstance}'
    payload = {
        "chatId": f"{chat_id}@c.us",
        "urlFile": image_url,
        "fileName": "image.jpg",
        "caption": caption
    }
    async with ClientSession() as session:
        response = await session.post(url, json=payload)
    return await response.json()
