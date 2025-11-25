from sqlalchemy import select
from database.models import User, async_session 

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            user = User(tg_id=tg_id)  # Создаем объект User
            session.add(user)
            await session.commit()
            print(f"✅ Пользователь {tg_id} добавлен в базу")
        else:
            print(f"ℹ️ Пользователь {tg_id} уже существует")

async def save_info_user(tg_id, target_time):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))        
        if user:
            user.target_time = target_time
            await session.commit()
            print(f"✅ Время напоминания для {tg_id} установлено: {target_time}")
        else:
            print(f"❌ Пользователь {tg_id} не найден")
