from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# 🛒 Рассчитать стоимость товара
# ❓Часто задаваемые вопросы
# 👨‍💻 Связаться с менеджером
# 📌 Отзывы покупателей
# 📱 Наши соц.сети

main_kb = [
    [KeyboardButton(text='🛒 Рассчитать стоимость товара'),
     KeyboardButton(text='👨‍💻 Связаться с менеджером')],
    [KeyboardButton(text='❓Часто задаваемые вопросы'),
     KeyboardButton(text='📌 Отзывы покупателей')],
    [KeyboardButton(text='📱 Наши соц.сети')]
]
main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже', )

go_back_kb = [[KeyboardButton(text='🔙 Назад в меню')]]
go_back = ReplyKeyboardMarkup(keyboard=go_back_kb, resize_keyboard=True)

otzivi = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='В Telegram', url='https://t.me/stufffeedback')],
    [InlineKeyboardButton(text='В VK', url='https://vk.com/romatruhov?w=wall330750798_272')]
])

FinalOrderR_KB = [
    [KeyboardButton(text='Добавить товар', callback_data='Добавить товар')],
    [KeyboardButton(text='Удалить товар', callback_data='Удалить товар')],
    [KeyboardButton(text='Отправить заявку менеджеру', callback_data='Менеджер, лови аптечку')],
    [KeyboardButton(text='Отменить заказ', callback_data='Галя, неси ключ, у нас отмена')]
]
FinalOrderR = ReplyKeyboardMarkup(keyboard=FinalOrderR_KB, one_time_keyboard=True,
                                  input_field_placeholder='Выберите вариант в меню ниже⬇️', resize_keyboard=True)

socials = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='VK', url='https://vk.com/romatruhov')],
    [InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/stuffmarketby')],
    [InlineKeyboardButton(text='TikTok', url='https://vm.tiktok.com/ZMNyuRqGt')]
])

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Adidas', callback_data='adidas')],
    [InlineKeyboardButton(text='Nike', callback_data='nike')]
])
shops_kb = [[KeyboardButton(text='Poizon'), KeyboardButton(text='Taobao'), KeyboardButton(text='1688')],
            [KeyboardButton(text='Pinduoduo'), KeyboardButton(text='95'), KeyboardButton(text='Другая площадка')],
            [KeyboardButton(text='Инструкция по установке приложений')], [KeyboardButton(text='Вернуться назад ⬅️️️')]]
shops = ReplyKeyboardMarkup(keyboard=shops_kb, one_time_keyboard=True,
                            input_field_placeholder='Выберите вариант в меню ниже⬇️', resize_keyboard=True)

inshop_back_kb = [[KeyboardButton(text='🔙 Назад в меню')]]
inshop_back = ReplyKeyboardMarkup(keyboard=inshop_back_kb, one_time_keyboard=True,
                                  input_field_placeholder='Сумма в юанях ¥', resize_keyboard=True)

inshop_kb = [
    [KeyboardButton(text='Оформить заказ 📝')],
    [KeyboardButton(text='Вернуться в меню ⬅️️️')]]
inshop = ReplyKeyboardMarkup(keyboard=inshop_kb, one_time_keyboard=False, resize_keyboard=True)

order_kb = [
    [KeyboardButton(text='Оформить ещё один товар')],
    [KeyboardButton(text='🔙 Назад в меню')]
]
order = ReplyKeyboardMarkup(keyboard=order_kb, one_time_keyboard=False, resize_keyboard=True)

faq_kb = [
    [KeyboardButton(text='Кто мы?'), ],
    [KeyboardButton(text='Как происходит расчёт?'), KeyboardButton(text='Стоимость и сроки доставки?')],
    [KeyboardButton(text='Как узнать нужный размер?')],
    [KeyboardButton(text='Вернуться в меню ⬅️️️')]
]
faq = ReplyKeyboardMarkup(keyboard=faq_kb, one_time_keyboard=False, resize_keyboard=True)
#  1. Poizon
#  2. Taobao
#  3. 1688
#  4. Pinduoduo
#  5. 95
#  6. Другая площадка
#  7. Инструкция по установке приложений
#  8. Вернуться назад ⬅️
