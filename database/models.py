from tortoise import fields
from tortoise.models import Model
from tortoise.validators import MinValueValidator



class User(Model):
    telegram_id = fields.IntField(unique=True)


class Exercise(Model):
    count = fields.SmallIntField(default=0, validators=[MinValueValidator(0)])
    exercise_date = fields.DatetimeField(auto_now_add=True)
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        model_name='models.User',
        related_name='exercises',
    )
