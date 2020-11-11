from loader import dp, db, bot
from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.utils.exceptions import MessageToDeleteNotFound
from misc.parse import info_station
from misc.keyboard import selection
from misc.dynamic_keyboard import DynamicButtons


@dp.message_handler(CommandStart())
async def start_send(message: Message):
    await message.answer('Добро пожаловать!\n'
                         'Это бот для Алматинского метрополитена!\n'
                         '<i>на котором я никогда в жизни не ездил :(</i>\n\n'
                         'Тут вы так-же можете ставить заметки для себя :3',
                         reply_markup=selection)
    if await db.exist_user(message.from_user.id) is False:
        await db.add_user(message.from_user.id)
    try:
        await bot.delete_message(message.from_user.id, message_id=message.message_id-1)
    except MessageToDeleteNotFound:
        pass
    await message.delete()


@dp.message_handler(CommandHelp())
async def help_send(message: Message):
    await message.answer('Автор🤡: @salvatttt', reply_markup=selection)
    if await db.exist_user(message.from_user.id) is False:
        await db.add_user(message.from_user.id)
    try:
        await bot.delete_message(message.from_user.id, message_id=message.message_id-1)
    except MessageToDeleteNotFound:
        pass
    await message.delete()


@dp.message_handler(text_contains='/')
async def choice_station(message: Message):
    message_text = message.text.replace('/', '')
    await message.delete()
    schedules = await info_station(message_text)
    testing = ['Load.']
    await message.answer(text=schedules, reply_markup=DynamicButtons(text=testing, callback=['time']).inline)

