import logging
import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from config_reader import config

# Лог в консоль
logging.basicConfig(level=logging.INFO)


# Polling, т.е. бесконечный цикл проверки апдейтов на серверах Telegram
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


# Функция main() запускается только при запуске скрипта из этого файла
if __name__ == '__main__':
    asyncio.run(main())
