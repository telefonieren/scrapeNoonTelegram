import time
import json

from aiogram.utils.markdown import hbold, hlink, hitalic

import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5344108083:AAFuOcFEprEmS_Ew7Hery7JKNMwjQTrH7F8'

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)


async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)


async def main():
    with open('final_result.json') as file:
        data = json.load(file)
        for item in data:
            card = f"{hlink(item.get('title'), item.get('link'))}\n" \
                   f"{hbold('Цена: ')} {hbold(item.get('new_price'))} 🔥\n" \
                   f"Старая цена: {item.get('old_price')}\n" \
                   f"{hbold('Общая скидка: ')}{hitalic(item.get('discount'))} 😍\n" \
 \
            await bot.send_message(-1001712092516, card, parse_mode=types.ParseMode.HTML)
            print(card)
            time.sleep(1400)
    file.close()


if __name__ == '__main__':
    asyncio.run(main())
