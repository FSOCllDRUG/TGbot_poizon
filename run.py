import asyncio
import datetime
import logging

from aiogram import Bot, Dispatcher

from app.handlers.admin_handlers import router as r2
from app.handlers.handlers import router as r1
from config_reader import config

# Получаем текущую дату и время
now = datetime.datetime.now()

# Форматируем в виде строки
now_str = now.strftime("%Y-%m-%d_%H-%M-%S")

# Добавляем к имени файла
log_filename = f'logs/bot_{now_str}.log'

logging.basicConfig(filename=log_filename, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# Polling, т.е. бесконечный цикл проверки апдейтов на серверах Telegram
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    # dp.include_routers(r1, r2)
    dp.include_router(r2)
    dp.include_router(r1)
    await dp.start_polling(bot)


# Функция main() запускается только при запуске скрипта из этого файла
if __name__ == '__main__':
    asyncio.run(main())
