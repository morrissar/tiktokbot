from aiogram.types import Message
import logging
import asyncio 
import os
from dotenv import load_dotenv
from handlers.admin import admin_router

load_dotenv()

from aiogram import Bot, Dispatcher
from handlers.user import user
from database.models import async_main
from scheduler import SimpleScheduler 

async def main():
    print("=== Бот запускается ===")
    print(f"Token: {'*' * 10}{os.getenv('TOKEN')[-4:] if os.getenv('TOKEN') else 'NOT FOUND'}")
    
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(user)
    dp.include_router(admin_router)
    await async_main()

    scheduler = SimpleScheduler(bot)
    scheduler_task = asyncio.create_task(scheduler.start())
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f'❌ Ошибка: {e}')
    finally:
        print("🛑 Останавливаем бота...")
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
