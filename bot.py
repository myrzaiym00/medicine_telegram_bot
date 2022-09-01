from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from decouple import config
import json

bot = Bot(token=config('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    mess = f'Здравствуйте, {message.from_user.first_name}! Введите название лекарства:'
    await bot.send_message(message.from_user.id, mess)

with open("drugs_dict.json") as file:
    drugs_dict = json.load(file)

@dp.message_handler(content_types=types.ContentType.TEXT)
async def find_medicine(message : types.Message):
    with open("drugs_dict.json") as file:
        drugs_dict = json.load(file)
    
    count = 0
    for k, v in drugs_dict.items():
        if message.text.lower() in k.lower():
            count += 1
            text = hlink(k, v)
            await bot.send_message(message.from_user.id, text, parse_mode='HTML')

    if count == 0:
        text = "К сожалению, мы не смогли найти это лекарство. Убедитесь, что название лекарства написано правильно." 
        await bot.send_message(message.from_user.id, text, parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp)