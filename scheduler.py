import asyncio
import datetime
from database.models import User, async_session
from sqlalchemy import select

class SimpleScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.is_running = False

    async def send_reminder(self, tg_id):
        """Отправка напоминания пользователю"""
        try:
            await self.bot.send_message(
                chat_id=tg_id,
                text="⏰ Напоминание! Пора продолжить серию в TikTok!"
            )
            print(f"✅ Напоминание отправлено пользователю {tg_id}")
        except Exception as e:
            print(f"❌ Ошибка отправки напоминания {tg_id}: {e}")

    async def check_reminders(self):
        """Проверка напоминаний"""
        try:
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            print(f"🕒 Проверка времени: {current_time}")
            
            async with async_session() as session:
                result = await session.execute(select(User).where(User.target_time.isnot(None)))
                users = result.scalars().all()
                print(f"👥 Найдено пользователей с напоминаниями: {len(users)}")
                
                for user in users:
                    print(f"🔍 Проверка {user.tg_id}: {user.target_time} == {current_time}")
                    if user.target_time == current_time:
                        print(f"🎯 СОВПАДЕНИЕ! Отправляю напоминание {user.tg_id}")
                        await self.send_reminder(user.tg_id)
        except Exception as e:
            print(f"❌ Ошибка в проверке напоминаний: {e}")

    async def start(self):
        """Запуск планировщика"""
        self.is_running = True
        print("✅ Планировщик запущен")
        
        while self.is_running:
            await self.check_reminders()
            await asyncio.sleep(30)

    async def stop(self):
        """Остановка планировщика"""
        self.is_running = False
        print("✅ Планировщик остановлен")
