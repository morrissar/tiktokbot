from aiogram import Router, Bot
from aiogram.types import Message, ReplyParameters
from aiogram import F
import keyboards.userkb as kb 

admin_router = Router()

@admin_router.message(F.chat.id == -1005002243682)
async def admin_reply(message: Message, bot: Bot):
    if message.reply_to_message and message.reply_to_message.forward_from:
        try:
            user_id = message.reply_to_message.forward_from.id
            
            await bot.send_message(chat_id=user_id, text=f"👨‍💻 Ответ поддержки: {message.text}", reply_markup=kb.main)
            await message.reply("✅ Ответ отправлен пользователю!")
            
        except Exception as e:
            await message.reply(f"❌ Ошибка: {e}")
