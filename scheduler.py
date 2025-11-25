import asyncio
import datetime
from database.models import User, async_session
from sqlalchemy import select

class SimpleScheduler:
    def __init__(self, bot):
        self.bot = bot
        self.is_running = False

    async def start(self):
        self.is_running = True       
        while self.is_running:
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
                await asyncio.sleep(30)
            except Exception as e:
                print(f"❌ Ошибка в планировщике: {e}")
                await asyncio.sleep(30)
