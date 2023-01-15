from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path
from pydub import AudioSegment
import numpy as np
import cv2
import configparser

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

@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def process_audio(message: types.Message):
    Path(f'voice_ogg/{message.from_user.id}').mkdir(parents=True, exist_ok=True)
    Path(f'voice_wav/{message.from_user.id}').mkdir(parents=True, exist_ok=True)
    voice = await message.voice.get_file()
    await bot.download_file(voice.file_path, destination = f'voice_ogg/{message.from_user.id}/{voice.file_id}.ogg')
    ogg = AudioSegment.from_ogg(f'voice_ogg/{message.from_user.id}/{voice.file_id}.ogg')
    ogg = ogg.set_frame_rate(16000)
    ogg.export(f'voice_wav/{message.from_user.id}/{voice.file_id}.wav', format="wav")
    await message.answer('Аудио сохранено!')

async def detect_face(img, message, file_id):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
    if len(faces) > 0:
        await message.answer('Лицо есть - фото сохранено!')
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        Path(f'facial_photos/{message.from_user.id}').mkdir(parents=True, exist_ok=True)   
        cv2.imwrite(f'facial_photos/{message.from_user.id}/{file_id}.jpg', img)
    else:
        await message.answer('Лица нет - фото не сохранено!')

@dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message):
    photo = await message.photo[-1].get_file()
    photo_buf = await bot.download_file(photo.file_path)
    img = cv2.imdecode(np.frombuffer(photo_buf.read(), np.uint8), 1)
    await detect_face(img, message, photo.file_id)

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    executor.start_polling(dp, skip_updates=True)