import random
import time
import json

from config import API_TOKEN, channel_id
from aiogram.utils.markdown import hbold, hlink, hitalic

#
#

import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types



# Configure logging
logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)



async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)

async def main():



    with open('final_result.json') as file:
        data = json.load(file)


        for item in data:
            smile_1 = random.choice(['😍', '🤩', '🤑', '😻', '🤪', '🤠', '🤫', '🥳'])
            smile_2 = random.choice(['⭐', '🌟', '💥', '🔥', '💐', '🌈', '🌞', '🍾', '🏆', '🏅'])
            card = f"{hlink(item.get('title'), item.get('link'))}\n" \
                   f"{hbold('Цена: ')} {hbold(item.get('new_price'))} {smile_1}\n" \
                   f"Старая цена: {item.get('old_price')}\n" \
                   f"{hbold('Общая скидка: ')}{hitalic(item.get('discount'))} {smile_2}\n" \


            await bot.send_message(channel_id, card, parse_mode=types.ParseMode.HTML)
            print(card)
            time.sleep(2800)
    file.close()





if __name__ == '__main__':
    asyncio.run(main())
