from aiogram.types import Message
import logging
import asyncio 
import os
from dotenv import load_dotenv
from typing import Callable, Dict, Any, Awaitable

load_dotenv()

from aiogram import Bot, Dispatcher, BaseMiddleware
from handlers.user import user
from database.models import async_main
from scheduler import SimpleScheduler 

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        result = await handler(event, data)
        return result

async def main():
    print("=== Бот запускается ===")
    print(f"Token: {'*' * 10}{os.getenv('TOKEN')[-4:] if os.getenv('TOKEN') else 'NOT FOUND'}")
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(user)
    
    await async_main()
    print("✅ База данных инициализирована")
    
    scheduler = SimpleScheduler(bot)
    scheduler_task = asyncio.create_task(scheduler.start())
    
    await bot.delete_webhook(drop_pending_updates=True)
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print('Бот выключен!')
    finally:
        await scheduler.stop()
        scheduler_task.cancel()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Бот включен!')
    try:
        asyncio.run(main()) 
    except KeyboardInterrupt:

        print('Бот выключен!')


