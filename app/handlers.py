from aiogram import Router, F
from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery
import keyboards as kb

router = Router()


class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in [6092344340, 1773979594]


# class Nastya(Filter):
#     async def __call__(self, message: Message) -> bool:
#         return message.from_user.id in [1773979594]


@router.message(Admin(), F.text == '/admin')
async def cmd_admin(message: Message):
    await message.answer('Вы админ.')


# Основная команда для запуска бота /start
@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer("U're welcome!", reply_markup=kb.main)


# Выдает пользователю его ID
@router.message(F.text == 'Мой ID')
async def cmd_my_id(message: Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
    await message.answer(f'Ваше имя: {message.from_user.first_name}')
    # await message.answer_photo(photo='https://linuxconfig.org/wp-content/uploads/2022/03/06-how-to-configure-static'
    #                                  '-ip-address-on-ubuntu-22-04-jammy-jellyfish-desktop-server.png',
    # caption='Пример отправки фото')


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


@router.message(Admin(), F.text == '/secretik')
async def cmd_secret143(message: Message):
    await message.answer('Подскажи, как можно сказать "I love you" так, чтобы при этом не использовать буквы?')


@router.message(Admin(), F.text == '143')
async def cmd_secret143(message: Message):
    await message.answer('Ты точно Настюша? -_-', reply_markup=kb.secret_143)


@router.callback_query(Admin(), F.data == 'secret_143')
async def cb_secret143(callback: CallbackQuery):
    await callback.answer('Я тебе поверю на слово...')
    await callback.message.answer_video(video='BAACAgIAAxkBAAOnZRoDMifIRwkegNXnc8d_V6SG4VMAApsxAAKIJdFIDFaXkHtfsuAwBA')


@router.callback_query(F.data == 'adidas')
async def cb_adidas(callback: CallbackQuery):
    await callback.answer('Вы выбрали бренд')
    await callback.message.answer(f'Вы выбрали {callback.data}')


@router.callback_query(F.data == 'nike')
async def cb_adidas(callback: CallbackQuery):
    await callback.answer('Вы выбрали бренд', show_alert=True)
    await callback.message.answer(f'Вы выбрали {callback.data}')


@router.message(F.video)
async def cmd_get_video_id(message: Message):
    await message.answer(message.video.file_id)


# Хэндлер без фильтра, отвечает в случае, если сообщение от пользователя не подошло
# ни под один фильтр
@router.message()
async def echo(message: Message):
    await message.answer('Ты несёшь какую-то хуйню, которую, слава Деду, я не умею понимать.')
