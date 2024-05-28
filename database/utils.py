import logging

from tortoise import Tortoise

from config import DATABASE_URL


async def init() -> None:
    await Tortoise.init(
        db_url=DATABASE_URL,
        modules={'models': ['database.models']}
    )
    await Tortoise.generate_schemas()
    logging.info("Tortoise inited!")