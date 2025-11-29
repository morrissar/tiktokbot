import types
from aiogram import Dispatcher, Router, Bot
import asyncio
import keyboards.userkb as kb 
from database.requests import set_user, save_info_user
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart 
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F

class Test(StatesGroup):
    target_time = State()

class Support(StatesGroup):
    waiting_for_question = State()

user = Router()

@user.message(CommandStart())
async def start(message: Message):
    await set_user(message.from_user.id)
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer_photo(photo='https://yt3.googleusercontent.com/zfLrkQRuN_NSn9axjTm2UxuWBKc3t8N1c3QOSPTBTqhwEEWpUj61YK3DQsMRZz_gARtievGS=s900-c-k-c0x00ffffff-no-rj', caption='Привет! Я бот "Продолжи серию в TikTok"! Я готов напомнать тебе об отправке сообщений своим друзьям! Используй кнопки для управления!', reply_markup=kb.main)

@user.message(F.text == 'Новое напоминание.')
async def new_reminder(message: Message, state: FSMContext):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer('Введите время напоминания в формате "HH:MM", например, 16:30. (Учитывайте часовой пояс МСК-3!)', reply_markup=kb.after_reminder)
    await state.set_state(Test.target_time)

@user.message(Test.target_time) 
async def save_reminder_time(message: Message, state: FSMContext):
    if message.text == 'Назад в меню.':
        await state.clear()
        await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
        await message.answer_photo(photo='https://yt3.googleusercontent.com/zfLrkQRuN_NSn9axjTm2UxuWBKc3t8N1c3QOSPTBTqhwEEWpUj61YK3DQsMRZz_gARtievGS=s900-c-k-c0x00ffffff-no-rj', caption='Привет! Я бот "Продолжи серию в TikTok"! Я готов напомнать тебе об отправке сообщений своим друзьям! Используй кнопки для управления!', reply_markup=kb.main)
        return
    time_text = message.text.strip()
    if len(time_text) != 5 or time_text[2] != ':':
        await message.answer("❌ Неверный формат времени! Используйте HH:MM (например: 14:30)")
        return
    try:
        hours_str, minutes_str = time_text.split(':')
        hours = int(hours_str)
        minutes = int(minutes_str)
    except ValueError:
        await message.answer("❌ Часы и минуты должны быть числами! Используйте HH:MM")
        return
    if hours < 0 or hours > 23:
        await message.answer("❌ Часы должны быть от 00 до 23!")
        return       
    if minutes < 0 or minutes > 59:
        await message.answer("❌ Минуты должны быть от 00 до 59!")
        return
    await state.update_data(target_time=time_text)
    data = await state.get_data()    
    await save_info_user(message.from_user.id, data["target_time"])     
    await state.clear()
    await message.answer(f"✅ Напоминание установлено на {time_text}!")
    
@user.message(F.text == 'Добавить серии с друзьями.')
async def add_friend_series(message: Message):
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer('В процессе добавления...', reply_markup=kb.after_friend_series)
                        
@user.message(F.text == 'Назад в меню.')
async def back_to_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.bot.send_chat_action(chat_id=message.from_user.id, action=ChatAction.TYPING)
    await message.answer_photo(photo='https://yt3.googleusercontent.com/zfLrkQRuN_NSn9axjTm2UxuWBKc3t8N1c3QOSPTBTqhwEEWpUj61YK3DQsMRZz_gARtievGS=s900-c-k-c0x00ffffff-no-rj', caption='Привет! Я бот "Продолжи серию в TikTok"! Я готов напомнать тебе об отправке сообщений своим друзьям! Используй кнопки для управления!', reply_markup=kb.main)

@user.message(F.text == 'Поддержка.')
async def help_command(message: Message, state: FSMContext):
    await message.answer('Напишите ваш вопрос или обращение, и мы скоро ответим! Для отмены нажмите кнопку "Отмена".', reply_markup=kb.after_help)
    await state.set_state(Support.waiting_for_question)

@user.message(Support.waiting_for_question)
async def process_support_question(message: Message, state: FSMContext, bot: Bot):
    if message.text.lower() == 'отмена':
        await state.clear()
        await message.reply("❌ Обращение отменено.", reply_markup=kb.main)
        return
    try:
        forwarded_msg = await bot.forward_message(chat_id=-1005002243682, from_chat_id=message.chat.id, message_id=message.message_id)
        support_data = {'user_id': message.from_user.id, 'original_message_id': message.message_id, 'support_message_id': forwarded_msg.message_id}
        await message.reply("✅ Ваше обращение отправлено в поддержку! Ожидайте ответа в этом чате.", reply_markup=kb.main)
    except Exception as e:
        await message.reply("❌ Произошла ошибка при отправке обращения.", reply_markup=kb.main)
        print(f"Ошибка: {e}")
    await state.clear()

