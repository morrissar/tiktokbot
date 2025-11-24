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
                async with async_session() as session:
                    result = await session.execute(select(User).where(User.target_time.isnot(None)))
                    users = result.scalars().all()                    
                    for user in users:
                        if user.target_time == current_time:
                            await self.send_reminder(user.tg_id)
                await asyncio.sleep(30)               
            except Exception as e:
                await asyncio.sleep(30)
    async def stop(self):
        self.is_running = False
    async def send_reminder(self, tg_id):
        await self.bot.send_message(chat_id=tg_id, text="⏰ Напоминание! Пора продолжить серию в TikTok! 🎬")