import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode
import json

# Токен бота, который вы получили от BotFather
API_TOKEN = '7529856876:AAHUijFYljpWrSNN-mSBUiXthItLsox2_rE'

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Словарь для хранения заметок пользователей
notes_db = {}

# Функция для сохранения заметок в файл
def save_notes():
    with open('notes.json', 'w') as f:
        json.dump(notes_db, f, indent=4)

# Функция для загрузки заметок из файла
def load_notes():
    global notes_db
    try:
        with open('notes.json', 'r') as f:
            notes_db = json.load(f)
    except FileNotFoundError:
        notes_db = {}

# Загружаем заметки при старте
load_notes()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для заметок. Используй команду /note, чтобы добавить заметку.")

@dp.message_handler(commands=['note'])
async def add_note(message: types.Message):
    user_id = str(message.from_user.id)
    note_text = message.get_args()

    if not note_text:
        await message.reply("Пожалуйста, добавь текст заметки после команды /note.")
        return

    # Добавляем заметку пользователя в базу данных
    if user_id not in notes_db:
        notes_db[user_id] = []
    
    notes_db[user_id].append(note_text)
    save_notes()

    await message.reply(f"Заметка добавлена: {note_text}")

@dp.message_handler(commands=['notes'])
async def list_notes(message: types.Message):
    user_id = str(message.from_user.id)

    # Получаем заметки пользователя
    if user_id in notes_db and notes_db[user_id]:
        notes_list = "\n".join(f"{idx + 1}. {note}" for idx, note in enumerate(notes_db[user_id]))
        await message.reply(f"Ваши заметки:\n{notes_list}", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("У вас нет сохраненных заметок.")

@dp.message_handler(commands=['clear'])
async def clear_notes(message: types.Message):
    user_id = str(message.from_user.id)

    # Очищаем заметки пользователя
    if user_id in notes_db:
        notes_db[user_id] = []
        save_notes()
        await message.reply("Все ваши заметки удалены.")
    else:
        await message.reply("У вас нет заметок для удаления.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
