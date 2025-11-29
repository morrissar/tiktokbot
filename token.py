import os
from aiogram import Bot

# Вставь свой токен прямо здесь
BOT_TOKEN = "8071068177:AAGywyrSJa-fk62GdMlI7xZgtdt5UO61qos"  # ЗАМЕНИ на реальный токен

async def test():
    try:
        bot = Bot(token=BOT_TOKEN)
        me = await bot.get_me()
        print(f"✅ Бот работает! Имя: @{me.username}")
        await bot.session.close()
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
