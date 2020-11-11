from misc.keyboard import update_back, selection
from loader import dp, bot, db
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from misc.parse import get_station
from aiogram.utils.exceptions import MessageNotModified, MessageToDeleteNotFound
from asyncio import sleep
from datetime import datetime


@dp.callback_query_handler(text=['schedule', 'update'])
async def show_schedule(call: CallbackQuery):
    schedule = await get_station()
    notes = await db.get_notes(call.from_user.id)
    if notes is None:
        notes = str()
    key = 1
    breaker = False
    text = str()
    now_sec = datetime.now().minute*60+datetime.now().second
    while True:
        new_value = list()
        value = schedule.get(key)
        if len(value) == 3:
            new_value.append([value[0],
                              str((int(value[1].split(':')[1])*60+int(value[1].split(':')[2]))-now_sec),
                              str((int(value[2].split(':')[1])*60+int(value[2].split(':')[2]))-now_sec)])
            text += new_value[0][0] + ' TIME: ' + new_value[0][1] + ' = ' + new_value[0][2] + '\n\n'
        elif len(value) == 2:
            new_value.append([value[0], str((int(value[1].split(':')[1])*60+int(value[1].split(':')[2]))-now_sec)])
            text += new_value[0][0] + ' TIME: ' + new_value[0][1] + '\n\n'
        else:
            breaker = True
        try:
            if 0 >= int(new_value[0][1]) or 0 >= int(new_value[0][2]):
                schedule = await get_station()
        except IndexError:
            if 0 >= int(new_value[0][1]):
                schedule = await get_station()
        new_value = list()
        if breaker:
            break
        key += 1
        if key > 9:
            key = 1
            now_sec += 1
            try:
                await call.message.edit_text(text=text, reply_markup=update_back)
            except MessageNotModified:
                pass
            await sleep(1)
            text = str()
    await call.answer(cache_time=5)


@dp.callback_query_handler(text='note')
async def notice(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_text('Напишите заметку:')
    except MessageNotModified:
        pass
    await state.set_state('notice')
    await call.answer(cache_time=0)


@dp.message_handler(state='notice')
async def note(message: Message, state: FSMContext):
    try:
        await bot.delete_message(message.from_user.id, message.message_id-1)
    except MessageToDeleteNotFound:
        pass
    if len(message.text) < 256:
        await db.set_notes(text=message.text, id=message.from_user.id)
        await message.answer('Заметка успешно добавлена!', reply_markup=selection)
    else:
        await message.answer('Ваша заметка слишком длинная', reply_markup=selection)
    await message.delete()
    await state.finish()


@dp.callback_query_handler(text='back')
async def backing(call: CallbackQuery):
    try:
        await call.message.edit_text('Добро пожаловать!\n'
                                     'Это бот для Алматинского метрополитена!\n'
                                     '<i>на котором я никогда в жизни не ездил :(</i>\n\n'
                                     'Тут вы так-же можете ставить заметки для себя :3',
                                     reply_markup=selection)
    except MessageNotModified:
        pass
    await call.answer(cache_time=0)

