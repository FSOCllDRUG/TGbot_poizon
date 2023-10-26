import json

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

# Список user_id администраторов
ADMIN_IDS = ["5559094874", "6092344340"]
router = Router()


@router.message(Command("check"))
async def am_i_admin(message: Message):
    if str(message.from_user.id) in ADMIN_IDS:
        await message.reply('Да, вы являетесь администратором.')
    else:
        await message.reply('Нет, вы не являетесь администратором.')


@router.message(Command("help"))
async def help_admin(message: Message):
    if str(message.from_user.id) not in ADMIN_IDS:
        # await message.reply('У вас нет прав для выполнения этой команды.')
        return
    await message.reply('Чтобы <b>увидеть</b> актуальные значения в боте:'
                        '  <code>/show</code>\n\n'
                        'Чтобы <b>установить</b> значение:\n'
                        '   Курс CNY->BYN: '
                        '<code>/set rate {значение}</code>\n'
                        '   Стоимость авто-доставки: '
                        '<code>/set avto {значение} </code>\n'
                        '   Стоимость авиа-доставки: '
                        '<code>/set avia {значение}</code>', parse_mode='HTML')


# @router.message(Command("get_data"))
async def get_admin_data():
    with open('app/data/data.json', 'r') as f:
        data = json.load(f)
    return data


@router.message(Command("set"))
async def set_data(message: Message):
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply('У вас нет прав для выполнения этой команды.')
        return

    try:
        _, key, value = message.text.split()
        value = float(value)
        data = await get_admin_data()
        data[key] = value
        with open('app/data/data.json', 'w') as f:
            json.dump(data, f)
        await message.reply('Данные успешно установлены.')
    except Exception as e:
        await message.reply('Ошибка при установке данных.')
        await message.reply(f'Текст ошибки\n{e}')


@router.message(Command("show"))
async def show_data(message: Message):
    if str(message.from_user.id) not in ADMIN_IDS:
        await message.reply('У вас нет прав для выполнения этой команды.')
        return

    try:
        data = await get_admin_data()
        await message.reply('\n'.join([f'{key}={value}' for key, value in data.items()]))
    except Exception as e:
        await message.reply('Ошибка при получении данных.')
        await message.reply(f'Текст ошибки\n{e}')
