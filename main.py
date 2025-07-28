from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

class Form(StatesGroup):
    Question = State()
    QuestionFormName = State()
    NumberPhone = State()
    Task = State()
    Sroki = State()

MAIN_CARD_BUTTONS_VERICIT = [
    ("Заказать Услугу", "m_zakaz"),
    ("Отзывы", "m_otzv"),
    ("Портфолио", "m_portfolio"),
]

def main_card_keyboard_vericitify():
    kb_builder = InlineKeyboardBuilder()
    for text, cb_data in MAIN_CARD_BUTTONS_VERICIT:
        kb_builder.button(text=text, callback_data=cb_data)
    kb_builder.adjust(1)
    return kb_builder.as_markup()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    kb_vericitify = main_card_keyboard_vericitify()
    await message.answer(
        "Добро пожаловать в бота для заказа услуг программиста!",
        reply_markup=kb_vericitify
    )

@dp.callback_query(F.data == "m_zakaz")
async def support(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите свое имя: ")
    await call.answer()
    await state.set_state(Form.QuestionFormName)

@dp.callback_query(F.data == "m_otzv")
async def send_reviews(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Отзывы: https://t.me/deltaOTZV")
    await call.answer()

@dp.callback_query(F.data == "m_portfolio")
async def send_portfolio(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Портфолио: https://t.me/deltaChannelRU/4")
    await call.answer()

MAIN_CARD_BUTTONS = [
    ("Хостинг", "r_Хостинг"),
    ("Телеграм мини приложение", "r_ТелеграмПриложение"),
    ("Телеграм Бот", "r_ТелеграмБот"),
    ("2D Инди Игра", "r_2DИграИнди"),
    ("Пк Приложение", "r_ПкПриложение"),
    ("ИИ Бот", "r_ИИбот"),
    ("Веб сайт", "r_ВебСайт"),
    ("Скрипт", "r_Скрипт"),
]

def main_card_keyboard():
    kb_builder = InlineKeyboardBuilder()
    for text, cb_data in MAIN_CARD_BUTTONS:
        kb_builder.button(text=text, callback_data=cb_data)
    kb_builder.adjust(1)
    return kb_builder.as_markup()

@dp.message(Form.QuestionFormName)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(nameUser=message.text)
    kb_strana = main_card_keyboard()
    await message.answer("Выберите услугу:", reply_markup=kb_strana)
    await state.set_state(None) 

@dp.callback_query(F.data.startswith("r_"))
async def process_menu_callback(call: CallbackQuery, state: FSMContext):
    action = call.data[len("r_"):]
    if action == "Хостинг" or action == "ИИбот":
        await call.message.answer("Сроки: 1-2 дня")
        await call.message.answer("Стоимость: 1400Руб")
    else:
        await call.message.answer("Сроки: 10-14 дней")
        await call.message.answer("Стоимость: 3600Руб")

    await call.message.answer("Введите свой номер телефон: ")
    await state.update_data(uslugaUser=action)
    await state.set_state(Form.NumberPhone)
    await call.answer()

@dp.message(Form.NumberPhone)
async def process_number(message: Message, state: FSMContext):
    await state.update_data(numberUser=message.text)
    await message.answer("Опишите задачу: ")
    await state.set_state(Form.Task)

@dp.message(Form.Task)
async def process_task(message: Message, state: FSMContext):
    await state.update_data(taskUser=message.text)
    await message.answer(
        "1. Введите 'Быстрые сроки' (6 дней + 500 Рублей за скорость)\n"
        "2. Или введите сроки, которые написаны в услуге"
    )
    await state.set_state(Form.Sroki)

@dp.message(Form.Sroki)
async def process_sroki(message: Message, state: FSMContext):
    await state.update_data(srokiUser=message.text)
    await message.answer("Заявка отправлена программисту, мы вам ответим в течение дня")
    data = await state.get_data()

    s = data.get('srokiUser')

    if s == "Быстрые сроки":
        sroki = "6 дней"
    else:
        sroki = s

    await message.answer(
        f"📝 Ваша заявка:\n\n"
        f"👤 Имя: {data.get('nameUser')}\n\n"
        f"✨ Услуга: {data.get('uslugaUser')}\n\n"
        f"📞 Номер телефона: {data.get('numberUser')}\n\n"
        f"📝 Задача: {data.get('taskUser')}\n\n"
        f"⏳ Сроки: {sroki}\n\n"
        f"✅ Заявка принята! Мы свяжемся с вами"
    )

    if data["uslugaUser"] == "Хостинг" or data["uslugaUser"] == "ИИбот":
        await message.answer("Стоимость: 1400 рублей")
    else:
        if data["srokiUser"] == "Быстрые сроки":
            await message.answer("Стоимость: 4100 рублей")
        else:
            await message.answer("Стоимость: 3600 рублей")

    await state.clear()

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
