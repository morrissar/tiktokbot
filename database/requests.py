from sqlalchemy import select
from database.models import User, async_session 

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def save_info_user(tg_id, target_time):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))        
        if user:
            user.target_time = target_time
            await session.commit()

@user.message(F.text == '/check_db')
async def check_db(message: Message):
    import os
    db_exists = os.path.exists('db.sqlite3')
    await message.answer(f"База данных: {'✅ существует' if db_exists else '❌ не найдена'}")

