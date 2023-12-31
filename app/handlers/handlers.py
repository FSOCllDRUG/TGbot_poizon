import logging

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InputMediaPhoto  # , FSInputFile

from app.keyboards import keyboards as kb
from app.modules.convert import convert_price as cvrt
from app.modules.convert import get_data

router = Router()


# @router.message(F.photo)
# async def cmd_get_photo_id(message: Message):
#    await #message.answer_photo(photo=message.photo[-1].file_id,caption=message.photo[-1].file_id)

class Order(StatesGroup):
    photo_id = State()
    link = State()
    price = State()


class FinalOrder:
    def __init__(self):
        self.photo_id = []
        self.link = []
        self.priceCNY = []
        self.priceBYN = []

    def clear(self):
        self.photo_id.clear()
        self.link.clear()
        self.priceCNY.clear()
        self.priceBYN.clear()

    def remove_item(self, item_number):
        # Удаление товара с выбранным номером из каждого списка
        self.photo_id.pop(item_number)
        self.link.pop(item_number)
        self.priceCNY.pop(item_number)
        self.priceBYN.pop(item_number)


class RemId(StatesGroup):
    item_id = State()


user_orders = {}


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


@router.message(F.text == 'Вернуться в меню ⬅️️️')
async def cmd_start(message: Message):
    order = user_orders.get(message.from_user.id, FinalOrder())
    if order is not None:
        order.clear()
    await message.answer(text=f"<b>🔎 Главное меню</b>", parse_mode=ParseMode.HTML,
                         reply_markup=kb.main)


@router.message(F.text == 'Вернуться назад ⬅️️️')
async def back_in_menu(message: Message):
    await message.answer(text=f"<b>🔎 Главное меню</b>", parse_mode=ParseMode.HTML,
                         reply_markup=kb.main)


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
    await message.answer('Выберите интересующий вопрос в меню.',
                         reply_markup=kb.faq)


@router.message(F.text == 'Кто мы?')
async def faq_who(message: Message):
    await message.answer(
        'Мы являемся посредником в работе с Китаем. Через нас вы можете заказать любой товар, с любого китайского '
        'сайта 🇨🇳')


@router.message(F.text == 'Как происходит расчёт?')
async def faq_price_calc(message: Message):
    data = get_data()
    vikup = data["vikup"]
    rate = data["rate"]
    await message.answer(f'Актуальный курс: 1¥ = {rate:.2f}BYN\nТ.е. стоимость в ¥ • {rate:.2f}BYN = стоимость вашей '
                         f'позиции в BYN\n\n+ {vikup:.0f}% комиссия выкупа (оплата товара, связь с продавцом и доставка по '
                         'Китаю)')


@router.message(F.text == 'Стоимость и сроки доставки?')
async def faq_price_delivery(message: Message):
    # data = get_data()
    # avia_price = data['avia']
    # avto_price = data['avto']
    await message.answer('За доставку из Китая вы оплачиваете по прибытии заказа к нам на склад в Беларусь\n\n'

                         '🚀 Сроки доставки - 3.5-4 недели\n\n'

                         '💰 Наши тарифы:\n'
                         'До 5кг - 14$/кг\n'
                         'От 5кг до 15кг - 12$/кг\n'
                         'От 15 до 40кг - 10$/кг\n'
                         'От 40кг - менее 10$/кг (условия оговариваются индивидуально)\n'
                         'Примечание: заказ взвешивается вместе с упаковкой, в которую упаковывают китайские поставщики (то есть, кроссовки с Poizon взвешиваются вместе с коробкой бренда и коробкой Poizon)')


@router.message(F.text == 'Как узнать нужный размер?')
async def faq_size(message: Message):
    await message.answer('Помощь в выборе размера оказывает наш менеджер каждому в индивидуальном '
                         'порядке. Если у вас возникли трудности при выборе размера, лучше всего сразу пишите ему 👉 '
                         '@stuffmarketmanager')


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


@router.message(F.text == '🔙 Назад в меню')
@router.message(F.text.casefold() == "🔙 Назад в меню")
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
        "Действие отменено",
        reply_markup=kb.main,
    )


@router.message(Converting.yuan_amount, F.text.isdigit() == True)
async def converting(message: Message, state: FSMContext) -> None:
    await state.update_data(yuan_amount=message.text)
    x = int(message.text)
    byn_rate = cvrt(x)
    # data = get_data()
    # avia_price = data['avia']
    # avto_price = data['avto']
    await message.answer(
        f"<b>Итоговая стоимость</b>: {byn_rate:.2f} BYN + доставка из Китая (оплачивается по прибытии товара в "
        f"Беларусь, чем больше вес, тем дешевле цена доставки за кг) + услуги почты",
        parse_mode='HTML',
        reply_markup=kb.inshop)
    await state.clear()


# {avto_price:.0f}  {avia_price:.0f} $

@router.message(Converting.yuan_amount)
async def incorrect_input_rasschet(message: Message) -> None:
    await message.reply(
        text="Требуется ввести цену (численное значение)"
    )


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
async def MGPoizon(message: Message, state: FSMContext):
    await message.answer(text='Введите стоимость товара в юанях (¥)\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAO_ZTrsGTTlZcev3YnTAAGdmbFj_wgkAAJRzzEbC0VgSZzzMLLqme5DAQADAgADeQADMAQ',
                        caption='1. Выберите нужный товар на <b>Poizon</b> и нажмите на правую нижнюю кнопку\n'
                                '2. Выберите нужный размер и напишите цену, которая показана первой',
                        parse_mode=ParseMode.HTML),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPAZTrsGTx3CWyn0tkgb25UGE5MCloAAlLPMRsLRWBJKuZjMGZeFOgBAAMCAAN5AAMwBA')

    ]
    await message.answer_media_group(media=media)
    await state.set_state(Converting.yuan_amount)
    # await state.clear()


# Taobao
@router.message(F.text == 'Taobao')
async def MGTaobao(message: Message, state: FSMContext):
    await message.answer(text='Введите стоимость товара в юанях (¥)\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPDZTrsLZkSGt_wV3Blv-g-rOXKBaUAAljPMRsLRWBJhg8YgZVTgkABAAMCAAN5AAMwBA',
                        caption='1. Выберите нужный товар на <b>Taobao</b> и нажмите на правую нижнюю кнопку\n'
                                '2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам '
                                'количество), которая показана сверху',
                        parse_mode=ParseMode.HTML),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPEZTrsLYwS063jPHZtMFhjDj5XjJcAAlnPMRsLRWBJY8ovzOvLNugBAAMCAAN5AAMwBA')

    ]
    await message.answer_media_group(media=media)
    await state.set_state(Converting.yuan_amount)


# 1688
@router.message(F.text == '1688')
async def MG1688(message: Message, state: FSMContext):
    await message.answer(text='Введите стоимость товара в юанях (¥)\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPHZTrsR8B_s-LGpX8M1GsZjSGnNIAAAlvPMRsLRWBJMQgiIxOpaBIBAAMCAAN5AAMwBA',
                        caption='1. Выберите нужный товар на <b>1688</b> и нажмите на правую нижнюю кнопку (обращайте '
                                'внимание на цену за определённое количество)\n'
                                '2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам '
                                'количество), которая показана снизу', parse_mode="HTML"),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPIZTrsR6vgeNBL9ZIe5aRPTK7DbxUAAlzPMRsLRWBJM-L2ehseVyMBAAMCAAN5AAMwBA')

    ]
    await message.answer_media_group(media=media)
    await state.set_state(Converting.yuan_amount)


# Pinduoduo
@router.message(F.text == 'Pinduoduo')
async def MGPinduoduo(message: Message, state: FSMContext):
    await message.answer(text='Введите стоимость товара в юанях (¥)\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPLZTrsVeDRVfXPJoGFVjtf3lRxEasAAmfMMRtNXGFJqxnNv7FEWtIBAAMCAAN3AAMwBA',
                        caption=' 1. Выберите нужный товар на <b>Pinduoduo</b>. В карточке товара снизу 2 кнопки (🔵 - '
                                'одиночная покупка, 🟢 - парная покупка)\n'
                                '2. Выберите нужный цвет/размер и напишите цену (или общую сумму за нужное вам '
                                'количество), которая показана сверху', parse_mode="HTML"),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPMZTrsVb1fc7FtXlky6l7Rq0UgTFMAAmjMMRtNXGFJ5NnU5IbVpKQBAAMCAAN3AAMwBA')

    ]
    await message.answer_media_group(media=media)
    await state.set_state(Converting.yuan_amount)


# 95
@router.message(F.text == '95')
async def MG95(message: Message, state: FSMContext):
    await message.answer(text='Введите стоимость товара в юанях (¥)\n'
                              '<i>❗️В случае, если вы хотите заказать несколько штук одной модели, вводите суммарное '
                              'число</i>', parse_mode="HTML", reply_markup=kb.inshop_back)
    media = [
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPPZTrsZuC7hxppPEQgxVd0bxLyEMkAArbQMRsLRWBJb2TcdQxCFb4BAAMCAAN3AAMwBA',
                        caption='1. Выберите понравившийся товар на <b>95</b> и нажмите на обведённую кнопку\n'
                                '2. Выберите нужный размер и напишите цену, которая показана на зелёной кнопке снизу',
                        parse_mode="HTML"),
        InputMediaPhoto(type='photo',
                        media='AgACAgIAAxkBAAPQZTrsZirUbQr1CO0sxS_P3sCko6kAArXQMRsLRWBJuMDqLBrzbUUBAAMCAAN3AAMwBA')

    ]
    await message.answer_media_group(media=media)
    await state.set_state(Converting.yuan_amount)


# Другая площадка
@router.message(F.text == 'Другая площадка')
async def AnotherMarketplace(message: Message):
    await message.answer(text='<b>Для заказа с любой другой площадки свяжитесь с нашим менеджером</b>\n👨‍💻 '
                              '@stuffmarketmanager', parse_mode="HTML", reply_markup=kb.main)


@router.message(F.text == ' Инструкция по установке приложений')
async def howto_install(message: Message):
    await message.answer(
        'По вопросам установки и использования приложений китайских площадок временно обращайтесь к '
        'менеджеру за помощью\n👉 @stuffmarketmanager')


@router.message(F.text == 'Оформить заказ 📝')
async def CreateOrder(message: Message, state: FSMContext):
    order = user_orders.get(message.from_user.id, FinalOrder())
    order.clear()
    await message.answer(
        text='Отправьте фотографию товара', reply_markup=kb.go_back
    )
    await state.set_state(Order.photo_id)


@router.message(F.text == 'Добавить товар')
async def CreateOrder(message: Message, state: FSMContext):
    await message.answer(
        text='Отправьте фотографию товара', reply_markup=kb.go_back
    )
    await state.set_state(Order.photo_id)


@router.message(Order.photo_id, F.photo)
async def Link(message: Message, state: FSMContext):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await message.answer('Отправьте ссылку на товар')
    await state.set_state(Order.link)


@router.message(Order.link)
async def Price(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer('Пришлите цену товара в юанях')
    await state.set_state(Order.price)


@router.message(Order.price, F.text.isdigit() == True)
async def Summary1(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    user_data = await state.get_data()
    x = float(user_data["price"])
    byn_rate = cvrt(x)

    # Получите экземпляр FinalOrder для этого пользователя или создайте новый
    order = user_orders.get(message.from_user.id, FinalOrder())

    order.link.append(user_data["link"])
    order.priceCNY.append(user_data["price"])
    order.photo_id.append(user_data["photo_id"])
    order.priceBYN.append(byn_rate)

    # Сохраните экземпляр обратно в словарь
    user_orders[message.from_user.id] = order
    await state.clear()
    await message.answer('Ваш заказ:', reply_markup=kb.FinalOrderR)
    if len(order.photo_id) == 1:
        await message.answer_photo(
            photo=order.photo_id[0],
            caption=f'🛒 <b>Товаров</b>: 1\n 1. {order.link[0]} | '
                    f'{order.priceBYN[-1]:.2f} BYN\n\n<b>Итоговая сумма</b>: '
                    f'{order.priceBYN[-1]:.2f} BYN\n\n 🚛 По прибытии товара в Беларусь вы '
                    f'оплачиваете за доставку Китай-Беларусь + за услуги почты до вас', parse_mode='HTML',
            reply_markup=kb.FinalOrderR
        )
    else:
        caption = f'🛒 <b>Товаров</b>: {len(order.photo_id)}\n'
        for i in range(len(order.photo_id)):
            caption += f'{i + 1}. {order.link[i]} | {order.priceBYN[i]:.2f} BYN\n'
        caption += (f'\n<b>Итоговая сумма</b>: {sum(order.priceBYN):.2f} BYN\n\n 🚛 По прибытии товара в Беларусь вы '
                    f'оплачиваете за доставку Китай-Беларусь + за услуги почты до вас')
        media = [
            InputMediaPhoto(type='photo',
                            media=order.photo_id[0],
                            caption=f'{caption}', parse_mode='HTML', )
        ]
        for i in range(1, len(order.photo_id)):
            media.append(InputMediaPhoto(type='photo', media=order.photo_id[i]))
        await message.answer_media_group(media)


@router.message(F.text == 'Удалить товар')
async def remID(message: Message, state: FSMContext):
    await message.answer('Укажите номер товара в списке, который нужно убрать')
    await state.set_state(RemId.item_id)


@router.message(RemId.item_id, F.text.isdigit() == True)
async def rm_remID(message: Message, state: FSMContext):
    await state.update_data(item_id=message.text)
    user_data = await state.get_data()
    x = int(user_data["item_id"]) - 1
    order = user_orders.get(message.from_user.id, FinalOrder())
    order.remove_item(x)
    if len(order.photo_id) >= 1:
        await message.answer('Ваш заказ:', reply_markup=kb.FinalOrderR)
        if len(order.photo_id) == 1:
            await message.answer_photo(
                photo=order.photo_id[0],
                caption=f'🛒 Товаров: 1\n 1. {order.link[0]} | '
                        f'{order.priceBYN[-1]:.2f} BYN\n\nИтоговая сумма: '
                        f'{order.priceBYN[-1]:.2f} BYN\n\n 🚛 По прибытии товара в Беларусь вы '
                        f'оплачиваете за доставку Китай-Беларусь + за услуги почты до вас', reply_markup=kb.FinalOrderR
            )

        else:
            caption = f'🛒 Товаров: {len(order.photo_id)}\n'
            for i in range(len(order.photo_id)):
                caption += f'{i + 1}. {order.link[i]} | {order.priceBYN[i]:.2f} BYN\n'
            caption += (f'\n<b>Итоговая сумма</b>: {sum(order.priceBYN):.2f} BYN\n\n 🚛 По прибытии товара в Беларусь '
                        f'Вы оплачиваете за доставку Китай-Беларусь + за услуги почты до вас')
            media = [
                InputMediaPhoto(type='photo',
                                media=order.photo_id[0],
                                caption=f'{caption}', parse_mode='HTML', reply_markup=kb.FinalOrderR)
            ]
            for i in range(1, len(order.photo_id)):
                media.append(InputMediaPhoto(type='photo', media=order.photo_id[i]))
            await message.answer_media_group(media)
            # await message.answer('Действия:', reply_markup=kb.FinalOrder)
    else:
        await message.answer('Ваш заказ пуст, создайте его снова', reply_markup=kb.main)


@router.message(F.text == 'Отправить заявку менеджеру')
async def order_to_manager(message: Message):
    order = user_orders.get(message.from_user.id, FinalOrder())
    if len(order.photo_id) != 0:
        await message.answer(
            text='Ваш заказ отправлен нашему менеджеру. Для ускорения процесса можете самостоятельно переслать сообщение со списком товаров \n👉 @stuffmarketby',
            reply_markup=kb.main)
        if message.from_user.id != 5559094874:
            if len(order.photo_id) == 1:
                await message.bot.send_photo(
                    photo=order.photo_id[0],
                    caption=f'🛒 <b>Товаров</b>: 1\n 1. {order.link[0]} | '
                            f'{order.priceBYN[-1]:.2f} BYN\n\n<b>Итоговая сумма</b>: '
                            f'{order.priceBYN[-1]:.2f} BYN\n\nЗаказ от: '
                            f'@{message.from_user.username}', parse_mode='HTML', chat_id=5559094874
                )
            else:
                caption = f'🛒 <b>Товаров</b>: {len(order.photo_id)}\n'
                for i in range(len(order.photo_id)):
                    caption += f'{i + 1}. {order.link[i]} | {order.priceBYN[i]:.2f} BYN\n'
                caption += (f'\n<b>Итоговая сумма</b>: {sum(order.priceBYN):.2f} BYN\n\nЗаказ от: '
                            f'@{message.from_user.username}')
                media = [
                    InputMediaPhoto(type='photo',
                                    media=order.photo_id[0],
                                    caption=f'{caption}', parse_mode='HTML')
                ]
                for i in range(1, len(order.photo_id)):
                    media.append(InputMediaPhoto(type='photo', media=order.photo_id[i]))
                await message.bot.send_media_group(media=media, chat_id=5559094874)
        order = user_orders.get(message.from_user.id, FinalOrder())
        order.clear()
        if message.from_user.username is None:
            await message.answer(
                'У вас нет userID, перешлите сообщение с заказом менеджеру\n👉@stuffmarketmanager')
    else:
        await message.answer('Ваш заказ пуст, создайте его снова.', reply_markup=kb.main)


@router.message(F.text == 'Отменить заказ')
async def order_to_manager(message: Message):
    order = user_orders.get(message.from_user.id, FinalOrder())
    order.clear()
    await message.answer('Ваш заказ отменён.\n\nВозвращаю Вас в главное меню.', reply_markup=kb.main)


@router.message(Order.price)
async def incorrect_input(message: Message):
    await message.reply(
        text="Требуется ввести цену(численное значение)"
    )


@router.message(Order.photo_id)
async def incorrect_input(message: Message):
    await message.reply(
        text="Требуется прислать фото"
    )


# Хэндлер без фильтра, отвечает в случае, если сообщение от пользователя не подошло
# ни под один фильтр
@router.message()
async def echo(message: Message):
    await message.answer('Я тебя не понимаю\nВозвращаю тебя в главное меню', reply_markup=kb.main)
