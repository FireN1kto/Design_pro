from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal

user_registrated = Signal()

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Оповещать при новых комментариях?')
    login = models.CharField(max_length=150, unique=True, null=True)
    full_name = models.CharField(max_length=150, null=True)
    class Meta(AbstractUser.Meta):
        pass