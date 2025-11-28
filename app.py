from aiogram.types import Message
import logging
import asyncio 
import os
import sys
from dotenv import load_dotenv
from handlers.admin import admin_router

load_dotenv()

from aiogram import Bot, Dispatcher
from handlers.user import user
from database.models import async_main
from scheduler import SimpleScheduler 

async def main():
    print("=== Бот запускается ===")
    
    # Получаем токен и проверяем его
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Отладочная информация
    print("🔍 Проверяем переменные окружения...")
    print(f"BOT_TOKEN присутствует: {'Да' if BOT_TOKEN else 'Нет'}")
    
    if BOT_TOKEN:
        print(f"Token: {'*' * 10}{BOT_TOKEN[-4:]}")
        print(f"Длина токена: {len(BOT_TOKEN)}")
    else:
        print("❌ Критическая ошибка: BOT_TOKEN не найден!")
        print("\n💡 Решение:")
        print("1. На хостинге установите переменную окружения BOT_TOKEN")
        print("2. Убедитесь, что имя переменной точно 'BOT_TOKEN'")
        print("3. Перезапустите приложение после установки переменной")
        return
    
    # Проверяем формат токена
    if ':' not in BOT_TOKEN:
        print("❌ Неверный формат токена! Должен содержать ':'")
        return
    
    try:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(user)
        dp.include_router(admin_router)
        await async_main()

        scheduler = SimpleScheduler(bot)
        scheduler_task = asyncio.create_task(scheduler.start())
        
        await bot.delete_webhook(drop_pending_updates=True)
        
        print("✅ Бот успешно запущен и готов к работе!")
        await dp.start_polling(bot)
        
    except Exception as e:
        print(f'❌ Ошибка при запуске бота: {e}')
        import traceback
        print(f"🔍 Детали ошибки: {traceback.format_exc()}")
    finally:
        print("🛑 Останавливаем бота...")
        if 'scheduler' in locals():
            if hasattr(scheduler, 'stop'):
                await scheduler.stop()
            else:
                scheduler.is_running = False
            
            if scheduler_task and not scheduler_task.done():
                scheduler_task.cancel()
                try:
                    await scheduler_task
                except asyncio.CancelledError:
                    pass
        
        if 'bot' in locals():
            await bot.session.close()
        print("✅ Бот остановлен")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('🚀 Бот включается...')
    try:
        asyncio.run(main()) 
    except KeyboardInterrupt:
        print('🛑 Бот выключен по команде пользователя!')
    except Exception as e:
        print(f'❌ Критическая ошибка: {e}')
