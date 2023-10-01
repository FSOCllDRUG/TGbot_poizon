from aiogram import Router, F
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
import keyboards as kb

router = Router()


class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [6092344340]


@router.message(Admin(), F.text == '/admin')
async def cmd_admin(message: Message):
    await message.answer('Вы админ.')

# Основная команда для запуска бота /start
@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer("U're welcome!", reply_markup=kb.main)


# Выдает пользователю его ID
@router.message(F.text == '/my_id')
async def cmd_my_id(message: Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
    await message.answer(f'Ваше имя: {message.from_user.first_name}')
    await message.answer_photo(photo='https://linuxconfig.org/wp-content/uploads/2022/03/06-how-to-configure-static'
                                     '-ip-address-on-ubuntu-22-04-jammy-jellyfish-desktop-server.png',
                               caption='Пример отправки фото')


# Пример работы отправки фото ботом
@router.message(F.text == '/send_image')
async def cmd_send_image(message: Message):
    await message.answer_photo(photo='https://cdn.britannica.com/19/213119-050-C81C786D/Grumpy-Cat-2015-memes.jpg',
                               caption='Пример отправки пикчи по URL.')
    await message.answer_photo(
        photo='AgACAgIAAxkBAAMyZRlaa52rP4LFlbzrBGz0fux_Vc0AApDQMRuIJclIv10ua5LvfdABAAMCAAN5AAMwBA',
        caption='Пикча по ID.')


# Выдает ID документа в БД телеграм
@router.message(F.document)
async def cmd_get_doc_id(message: Message):
    await message.answer(message.document.file_id)


# Пример отправки документа по его ID
@router.message(F.text == '/send_doc')
async def cmd_send_doc(message: Message):
    await message.answer_document(document='BQACAgIAAxkBAAM3ZRlb3mfE770PiakyZpbM6Kr5UwYAAi86AAKIJclIGmRjBCu7l7IwBA')


# Выдаёт ID фото в БД Telegram
@router.message(F.photo)
async def cmd_get_photo_id(message: Message):
    await message.answer(message.photo[-1].file_id)


@router.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer('Дедовы контакты:', reply_markup=kb.socials)


@router.message(F.text == 'Каталог')
async def catalog(message: Message):
    await message.answer('Выберите бренд', reply_markup=kb.catalog)


@router.callback_query(F.data == 'adidas')
async def cb_adidas(callback: CallbackQuery):
    await callback.answer('Вы выбрали бренд')
    await callback.message.answer(f'Вы выбрали {callback.data}')


@router.callback_query(F.data == 'nike')
async def cb_adidas(callback: CallbackQuery):
    await callback.answer('Вы выбрали бренд', show_alert=True)
    await callback.message.answer(f'Вы выбрали {callback.data}')


# Хэндлер без фильтра, отвечает в случае, если сообщение от пользователя не подошло
# ни под один фильтр
@router.message()
async def echo(message: Message):
    await message.answer('Ты несёшь какую-то хуйню, которую слава богу я не умею понимать.')
