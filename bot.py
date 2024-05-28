import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TG_TOKEN
from database.models import Exercise, User
from database.utils import init
from services import get_amount_for_all_time, get_amount_for_n_days

telegram_bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user, _ = await User.get_or_create(telegram_id=message.from_user.id)
    logging.info(f"User with tg_id {user.telegram_id} created")
    await message.answer(
        f"Привет, {message.from_user.full_name}! Отправь мне количество повторений.",
    )


@dp.message(F.text)
async def handle_exercise(message: Message) -> None:
    repetitions: int
    try:
        repetitions = int(message.text)
    except ValueError:
        logging.warning(f"Sent wrong value {message.text}")
        await message.answer("Принимаются только числа, остальное все игнорируется.")
        return

    user_instance = await User.get_or_none(telegram_id=message.from_user.id)
    if user_instance is None:
        await message.answer("Вы не нажали кнопку /start.")
        return

    await Exercise.create(count=repetitions, user=user_instance)
    logging.info(f"User with tg_id {user_instance.telegram_id} create exercise with repetitions {repetitions}")

    total_repetitions = await get_amount_for_all_time(user_instance)
    month_repetitions = await get_amount_for_n_days(30, user_instance)
    week_repetitions = await get_amount_for_n_days(7, user_instance)

    await message.answer(
        (
            "Записано.\n"
            f"За неделю сделано {week_repetitions.total} раз.\n"
            f"За месяц сделано {month_repetitions.total} раз.\n"
            f"Всего сделано {total_repetitions.total} раз."
        )
    )


async def on_startup():
    logging.info("Init DB")
    await init()
    logging.info("DB init completed")


async def main():
    await on_startup()
    await dp.start_polling(telegram_bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
