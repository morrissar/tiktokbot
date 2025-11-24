from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Новое напоминание.')],
    [KeyboardButton(text='Добавить серии с друзьями.')]
],  resize_keyboard=True,
    input_field_placeholder='Не забывай про серию!')

after_reminder = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text='Назад в меню.')]
    ], resize_keyboard=True, input_field_placeholder='Управление напоминаниями...')

after_friend_series = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text = 'Назад в меню.')]
    ], resize_keyboard=True, input_field_placeholder='Управление сериями с друзьями...')