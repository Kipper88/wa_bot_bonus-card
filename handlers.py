import re
from utils import check_user, insert_user, send_image, send_message
from states import StateUser
from time import time

async def handle_message(chat_id, message):
    user = await check_user(chat_id)
    
    birthday_pattern = r'^((?:0[0-9]|[1-2][0-9]|3[0-1])([. ]))((?:0[1-9]|1[0-2])([. ]))((?:19|20)\d{2})$'    
    
    if re.match(birthday_pattern, message) and chat_id in StateUser.birthday:
        bday = message            
        user_data = {
            'id': 0,
            'username': 'User',
            'phone': str(chat_id),
            'balance': 0,
            'status': 'Серебряная ⚪️',
            'stamp': '',
            'bday': bday
        }
        await insert_user(user_data)
        await send_image(chat_id, 
                        image_url="https://i.postimg.cc/MprwdCcK/photo.jpg", 
                        caption="Вы успешно зарегистрированы.\nВаша карта:\n\nСтатус: Серебряная ⚪️\nБаланс: 0 Б\nШтампы:\n\nНапишите «Моя карта» без кавычек, чтобы обновить актуальные данные карты.")
        del StateUser.birthday[chat_id]
        
    elif message.lower() == "зарегистрироваться":
        if not user:
            if chat_id not in StateUser.birthday:
                await send_message(chat_id=chat_id,
                                   message='Чтобы зарегистрироваться, пожалуйста, напишите свою дату рождения в формате ДД.ММ.ГГГГ\nПример: 10.01.1900')
                StateUser.birthday[chat_id] = time()
        else:
            user = user[0]
            await send_image(chat_id,
                             f"Вы уже зарегистрированы.\nВаша карта:\n\nСтатус: {user['status']}\nБаланс: {user['balance']} Б\nШтампы:\n{user['stamp']}\n\nНапишите «Моя карта» без кавычек, чтобы обновить актуальные данные карты.", 
                             image_url="https://i.postimg.cc/MprwdCcK/photo.jpg")
        
    elif message.lower() == "моя карта":     
        if user:
            user = user[0]
            await send_image(chat_id, 
                       caption=f"Ваша карта:\n\nСтатус: {user['status']}\nБаланс: {user['balance']} Б\nШтампы:\n{user['stamp']}\n\nНапишите «Моя карта» без кавычек, чтобы обновить актуальные данные карты.",
                       image_url="https://i.postimg.cc/MprwdCcK/photo.jpg"
                       )
            pass
        else:
            await send_message(chat_id, "Вы не зарегистрированы. Чтобы зарегистрироваться напишите 'Зарегистрироваться'")
            
    elif chat_id in StateUser.birthday:
        await send_message(chat_id, "Вы ввели дату в неверном формате! Попробуйте еще раз. Формат - ДД.ММ.ГГГГ\nПример: 10.01.1900")
            
    else:
        await send_message(chat_id, "Неизвестная команда.\n\nНапишите «Зарегистрироваться», чтобы зарегистрироваться\nИли «Моя карта» если она у Вас уже Есть")
