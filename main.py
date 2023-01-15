from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
config_obj = configparser.ConfigParser()
config_obj.read('config.ini')
bot_param = config_obj['BOT']
BOT_TOKEN = bot_param['bot_token']

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    button = KeyboardButton('Что ты умеешь, бот?')
    markup = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True)
    markup.add(button)
    await message.answer(f'Привет, {message.from_user.first_name}!\n\nЯ чат-бот, сделан для ID R&D.', reply_markup = markup)

@dp.message_handler(text = ['Что ты умеешь, бот?'])
async def buttons(message: types.Message):
    inline_button = InlineKeyboardButton('Тык-тык!', callback_data='btn1')
    inline_markup = InlineKeyboardMarkup().add(inline_button)
    inline_markup.add(InlineKeyboardButton('Я на Github', url = 'https://github.com/riri-pythonissam'))
    await message.answer('Я умею сохранять голосовые сообщения и фотографии, на которых изображены лица людей.', reply_markup = inline_markup)
@dp.callback_query_handler(lambda c: c.data.startswith('btn'))
async def callback_btn(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Я бабака!')
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)