import time
import json

from aiogram import Dispatcher, Bot, executor, types
from aiogram.utils.markdown import hbold, hlink, hitalic
import os


bot = Bot(token='5344108083:AAFuOcFEprEmS_Ew7Hery7JKNMwjQTrH7F8', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Привет! Я бот noon.com')
    time.sleep(2)
    while True:
        time.sleep(10)
        with open('clothing-16021.json') as file:
            data = json.load(file)
            for item in data:
                card = f"{hlink(item.get('title'),item.get('link'))}\n" \
                    f"{hbold('Цена: ')} {hbold(item.get('new_price'))} 🔥\n" \
                    f"Старая цена: {item.get('old_price')}\n" \
                    f"{hbold('Общая скидка: ')}{hitalic(item.get('discount'))} 😍"
                await message.answer(card)
        file.close()


def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()