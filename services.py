from datetime import datetime, timedelta

from tortoise import functions

from database.models import Exercise, User


async def get_amount_for_n_days(n: int, user: User) -> int:
    now = datetime.now()
    n_days_ago = now - timedelta(days=n)
    return await (
        Exercise
        .filter(user=user, exercise_date__gte=n_days_ago)
        .annotate(total=functions.Sum('count')).get()
    )


async def get_amount_for_all_time(user: User) -> int:
    return await Exercise.filter(user=user).annotate(total=functions.Sum('count')).get()