from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from django.core.exceptions import ValidationError

user_registrated = Signal()

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Оповещать при новых комментариях?')
    login = models.CharField(max_length=150, unique=True, null=True)
    full_name = models.CharField(max_length=150, null=True)
    has_logged_in = models.BooleanField(default=False)

    def activation_status(self):
        if self.is_activated:
            return "Активный" if self.has_logged_in else "Неактивный"
        return "Неактивен"


    class Meta(AbstractUser.Meta):
        pass

def validate_image(image):
    if image.size > 2 * 1024 * 1024:  # 2 MB
        raise ValidationError('Размер изображения не должен превышать 2 Мб.')

class Category(models.Model):
    name = models.CharField(max_length=100)

class InteriorDesignRequest(models.Model):
    STATUS_CHOICES = [
        ('Новая', 'Новая'),
        ('В процессе', 'В процессе'),
        ('Завершена', 'Завершена'),
    ]
    name = models.CharField(max_length=100, verbose_name="Название заявки")
    email = models.EmailField(verbose_name="Ваш email")
    phone = models.CharField(max_length=15, verbose_name="Ваш телефон")
    project_description = models.TextField(verbose_name="Описание заявки")
    design_image = models.ImageField(upload_to='design_images/', validators=[validate_image], verbose_name="Фото помещения")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Новая', verbose_name="Статус")
    user = models.ForeignKey(AdvUser ,on_delete=models.CASCADE)

    def __str__(self):
        return f"Заявка от {self.name}, Статус {self.status}"