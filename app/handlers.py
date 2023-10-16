import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InputMediaPhoto  # , FSInputFile
from app.convert import convert_currency_async as cvrt
import keyboards as kb

router = Router()


class OrderForm(StatesGroup):
    photo_id = State()
    link = State()
    price = State()


class Converting(StatesGroup):
    yuan_amount = State()


# Основная команда для запуска бота /start
@router.message(F.text == '/start')
async def cmd_start(message: Message):
    await message.answer(text=f"<b>🔎 Главное меню</b>", parse_mode=ParseMode.HTML,
                         reply_markup=kb.main)


@router.message(F.text == 'Вернуться назад ⬅️️️')
async def back_in_menu(message: Message):
    await message.answer("Ты вновь в главном меню!", reply_markup=kb.main)


@router.message(F.text == '🛒 Рассчитать стоимость товара')
async def shops(message: Message):
    await message.answer(text=f'Выберите площадку, с которой вы хотели бы оформить заказ\n❗️<i>На каждой площадке </i>'
                              f'<i>присутствует поиск по фото</i>', parse_mode=ParseMode.HTML)
    await message.answer(text=f'Для того чтобы ознакомиться с инструкцией по установке приложений, нажмите на кнопку '
                              f'<b>«Инструкция по '
                              'установке приложений»</b>', parse_mode=ParseMode.HTML)
    await message.answer(text=f'<i>Если у вас возникают трудности при поиске товара или расчёта стоимости - наш '
                              f'менеджер с '
                              'радостью вам поможет</i>\n👉@stuffmarketmanager', parse_mode=ParseMode.HTML,
                         reply_markup=kb.shops)


@router.message(F.text == '👨‍💻 Связаться с менеджером')
async def contact_manager(message: Message):
    await message.answer(
        text=f'По всем вопросам вы можете обращаться к нашему менеджеру\n👉 @stuffmarketmanager\n\n<i>Также он может '
             f'помочь вам найти желаемый товар или полностью сопроводить оформление заказа, если у вас возникают '
             f'трудности </i>',
        parse_mode=ParseMode.HTML)


@router.message(F.text == '❓Часто задаваемые вопросы')
async def contact_manager(message: Message):
    await message.answer('❓Часто задаваемые вопросы\n\nКто мы?\n\nМы являемся посредником в работе с Китаем. Через '
                         'нас вы можете заказать любой товар, с любого китайского сайта 🇨🇳\n\n\nКак происходит '
                         'расчёт?\n\nАктуальный курс: 1¥ = 0.53BYN\nТ.е. стоимость в ¥ • 0.53BYN = стоимость вашей '
                         'позиции в BYN\n\n+ 5% комиссия выкупа (оплата товара, связь с продавцом и доставка по '
                         'Китаю)\n\n\nСтоимость и сроки доставки?\n\nЗа доставку из Китая в Беларусь вы оплачиваете '
                         'по прибытии заказа к нам\n\nНаши тарифы:\nАвиа-доставка (20-30 дней до Беларуси) - '
                         '10$/кг\nАвто-доставка (40-50 дней до Беларуси) - временно недоступна ⏳\n\nПримечание: заказ '
                         'взвешивается вместе с упаковкой, в которую упаковывают китайские поставщики\n\n\nКак узнать '
                         'нужный размер?\n\nПомощь в выборе размера оказывает наш менеджер каждому в индивидуальном '
                         'порядке. Если у вас возникли трудности при выборе размера, лучше всего сразу пишите ему 👉 '
                         '@stuffmarketmanager',
                         reply_markup=kb.main)


@router.message(F.text == '📌 Отзывы покупателей')
async def contact_manager(message: Message):
    await message.answer('Посмотрите, что пишут о нас наши клиенты', reply_markup=kb.otzivi)


@router.message(F.text == '📱 Наши соц.сети')
async def contacts(message: Message):
    await message.answer('Наши соц.сети:', reply_markup=kb.socials)


@router.message(F.text == 'Инструкция по установке приложений')
async def instruction(message: Message):
    await message.answer(
        'По вопросам установки и использования приложений китайских площадок временно обращайтесь к менеджеру за '
        'помощью 👉 @stuffmarketmanager', reply_markup=kb.main)


@router.message(F.text == '🔙Назад')
@router.message(F.text.casefold() == "🔙Назад")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=kb.shops,
    )


@router.message(Converting.yuan_amount)
async def converting(message: Message, state: FSMContext) -> None:
    await state.update_data(yuan_amount=message.text)
    # x = await state.get_data()
    while True:
        try:
            x = float(message.text)
            byn_rate = await cvrt(x / 10 * 1.05, 'CNY')
            usd_byn_rate_avia = await cvrt(10, 'USD')
            usd_byn_rate_avto = await cvrt(5, 'USD')
            await message.answer(
                f"Цена товара= {byn_rate:.2f} BYN\nЦена авто-доставки за 1 кг= {usd_byn_rate_avto:.2f} BYN\nЦена "
                f"авиа-доставки за 1 кг= {usd_byn_rate_avia:.2f} BYN", reply_markup=kb.inshop)
            await state.clear()
            break
        except ValueError:
            await message.answer("Возврат в главное меню", reply_markup=kb.main)
            await state.clear()
            break


@router.message(Converting.yuan_amount)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("I don't understand you :(")


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


@router.message(F.video)
async def cmd_get_video_id(message: Message):
    await message.answer(message.video.file_id)


# Poizon
@router.message(F.text == 'Poizon')
async def PoizonMG(message: Message, state: FSMContext):
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICRWUr1hgkiFedWNhRvy1_XOqOlio2AAJRzzEbC0VgSV39HkLjH8KAAQADAgADeQADMAQ',
                        caption='1. Выберите нужный товар на Poizon и нажмите на правую нижнюю кнопку\n'
                                '2. Выберите нужный размер и напишите цену, которая показана первой'),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICR2Ur1h-7-Zv7kwsIyuGh7qa69GBVAAJSzzEbC0VgSRmaM9d8YOtYAQADAgADeQADMAQ')

    ]
    await message.answer_media_group(media=media)
    await message.answer(text='Введите стоимость товара в юанях ¥\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)

    await state.set_state(Converting.yuan_amount)
    # await state.clear()


# Taobao
@router.message(F.text == 'Taobao')
async def PoizonMG(message: Message, state: FSMContext):
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICSWUr1ik8MDLMv-sp4GqxTA6uYz0lAAJYzzEbC0VgST83L4RIXXNGAQADAgADeQADMAQ',
                        caption='1. Выберите нужный товар на Taobao и нажмите на правую нижнюю кнопку\n'
                                '2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам количество), которая показана сверху'),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICS2Ur1jfq17flEjLqRlC7fe_-zYxQAAJZzzEbC0VgSR1_rmZUM5QjAQADAgADeQADMAQ')

    ]
    await message.answer_media_group(media=media)
    await message.answer(text='Введите стоимость товара в юанях ¥\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)

    await state.set_state(Converting.yuan_amount)


# 1688
@router.message(F.text == '1688')
async def PoizonMG(message: Message, state: FSMContext):
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICTWUr1kHh6NovpXnH0bXhAxRt100PAAJbzzEbC0VgSZP4DgOTl1gmAQADAgADeQADMAQ',
                        caption='1. Выберите нужный товар на 1688 и нажмите на правую нижнюю кнопку (обращайте '
                                'внимание на цену за определённое количество)\n'
                                '2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам '
                                'количество), которая показана снизу'),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICT2Ur1kZAw_RmEu8GLQAB9nOsGJqPhAACXM8xGwtFYEk_IATFQY1w7wEAAwIAA3kAAzAE')

    ]
    await message.answer_media_group(media=media)
    await message.answer(text='Введите стоимость товара в юанях ¥\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)

    await state.set_state(Converting.yuan_amount)


# Pinduoduo
@router.message(F.text == 'Pinduoduo')
async def PoizonMG(message: Message, state: FSMContext):
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICVWUr1nKAI8FKSCStIsAQMgOJe9MiAAJnzDEbTVxhSXm_4FIqXoIRAQADAgADdwADMAQ',
                        caption=' 1. Выберите нужный товар на Pinduoduo. В карточке товара снизу 2 кнопки (🔵 - одиночная покупка, 🟢 - парная покупка)\n'
                                '2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам количество), которая показана сверху'),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICV2Ur1nJVLYKDu0sv5ZPZo5MhZrwfAAJozDEbTVxhSUyDMx4dbjUuAQADAgADdwADMAQ')

    ]
    await message.answer_media_group(media=media)
    await message.answer(text='Введите стоимость товара в юанях ¥\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)

    await state.set_state(Converting.yuan_amount)


# 95
@router.message(F.text == '95')
async def PoizonMG(message: Message, state: FSMContext):
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICWmUr1sgd6MNEeCz1Wi2cWfX7tMAtAAK20DEbC0VgSTxc7Fvw8TqdAQADAgADdwADMAQ',
                        caption='1. Выберите понравившийся товар на 95 и нажмите на обведённую кнопку\n'
                                '2. Выберите нужный размер и напишите цену, которая показана на зелёной кнопке снизу'),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAICWWUr1sc7bmf5x41W7kduoO-a3z7-AAK10DEbC0VgSUJYref0ncrtAQADAgADdwADMAQ')

    ]
    await message.answer_media_group(media=media)
    await message.answer(text='Введите стоимость товара в юанях ¥\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)

    await state.set_state(Converting.yuan_amount)


# Другая площадка
@router.message(F.text == 'Другая площадка')
async def AnotherMarketplace(message: Message):
    await message.answer(text='<b>Для заказа с любой другой площадки свяжитесь с нашим менеджером</b>\n👨‍💻 '
                              '@stuffmarketmanager', parse_mode="HTML", reply_markup=kb.main)


@router.message(F.text == ' Инструкция по установке приложений')
async def howto_install(message: Message):
    await message.answer('По вопросам установки и использования приложений китайских площадок временно обращайтесь к '
                         'менеджеру за помощью\n👉 @stuffmarketmanager')


# Отправка заявки на оформление заказа
@router.message(F.text == 'Оформить заказ 📝')
@router.message(F.text == 'Оформить ещё один товар')
async def CreateOrder(message: Message, state: FSMContext):
    await message.answer(
        text='Отправьте скриншот выбранного товара', reply_markup=kb.go_back
    )
    await state.set_state(OrderForm.photo_id)


@router.message(OrderForm.photo_id, F.photo)
async def Price(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer('Пришлите ссылку на выбранный товар')
    await state.set_state(OrderForm.link)


@router.message(OrderForm.link)
async def Photo(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer('Пришлите цену товара в юанях')
    await state.set_state(OrderForm.price)


@router.message(OrderForm.price)
async def Summary(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    user_data = await state.get_data()
    x = float(user_data["price"])
    byn_rate = await cvrt(x / 10 * 1.05, 'CNY')
    await message.answer_photo(str(user_data["photo_id"]),
                               caption=f'Ссылка на товар: \n {user_data["link"]} \nЦена товара:\n'
                                       f' {user_data["price"]}¥= {byn_rate:.2f}BYN', reply_markup=kb.order)
    await message.answer('Ваша заявка отправлена менеджеру 👉 @stuffmarketmanager')
    if message.from_user.id != 5559094874:
        await message.bot.send_photo(photo=str(user_data["photo_id"]),
                                     caption=f'Ссылка на товар: {user_data["link"]} \nЦена товара:'
                                             f' {user_data["price"]}¥ = '
                                             f'{byn_rate:.2f}BYN\nЗаказ от: '
                                             f'@{message.from_user.username}',
                                     chat_id=5559094874)


# Хэндлер без фильтра, отвечает в случае, если сообщение от пользователя не подошло
# ни под один фильтр
@router.message()
async def echo(message: Message):
    await message.answer('Я тебя не понимаю\nВозвращаю тебя в главное меню.', reply_markup=kb.main)
