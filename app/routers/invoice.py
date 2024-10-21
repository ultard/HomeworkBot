from os import getenv

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery

invoices_router = Router()

# Обработчик для создания invoice
@invoices_router.message(Command("buy"))
async def process_buy_command(message: Message):
    prices = [
        LabeledPrice(label="Подписка", amount=100_00)
    ]

    await message.answer_invoice(
        title="Плоти налоги",
        description="Налоги платим",
        payload="bot-defined-invoice-payload",
        provider_token=getenv('PAYMENT_TOKEN'),
        currency="RUB",
        prices=prices,
        start_parameter="time-machine-example",
    )

# Обработчик успешной оплаты
@invoices_router.pre_checkout_query(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

# Обработчик успешного платежа
@invoices_router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment_info = message.successful_payment
    print(f"Успешный платеж: {payment_info}")
    await message.answer(f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} был успешно проведен!")
