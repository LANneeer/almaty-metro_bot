from loader import db
from set_commands import set_bot_commands
import logging

logging.basicConfig(level=logging.INFO)


async def on_startup(dp):
    await db.create_table()
    await set_bot_commands(dp)

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
