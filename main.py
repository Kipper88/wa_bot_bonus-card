import asyncio
from flask import Flask, request
import time

from handlers import handle_message
from states import StateUser
    
app = Flask(__name__)

@app.route('/', methods=['POST'])
async def webhook():
    data = request.json
    
    if data['messageData']['typeMessage'] == 'textMessage':
        chat_id = data['senderData']['chatId'].split('@')[0]
        text = data['messageData']['textMessageData']['textMessage']
        await handle_message(chat_id, text)
    return "OK", 200

async def checker_state():
    while True:
        for i in StateUser.birthday:
            if StateUser.birthday[i] < time.time - 10: # 15 мин
                del StateUser.birthday[i]
        await asyncio.sleep(60)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(checker_state())
    app.run(debug=True)
