import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router


# Polling, т.е. бесконечный цикл проверки апдейтов на серверах Telegram
async def main():
    bot = Bot(token='6421951776:AAH5n4G5DsXFkRainmE7vFhENEeg6WEi6tI')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


# Функция main() запускается только при запуске скрипта из этого файла
if __name__ == '__main__':
    asyncio.run(main())
