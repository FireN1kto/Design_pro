from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import Signal
from django.core.exceptions import ValidationError

user_registrated = Signal()

class AdvUser(AbstractUser):
    STATUS_CHOICES = [
        ('offline', 'Не живой'),
        ('online', 'Живой'),
    ]
    is_activated = models.BooleanField(default=False, verbose_name='Прошел активацию?')
    send_messages = models.BooleanField(default=True, verbose_name='Оповещать при новых комментариях?')
    username = models.CharField(max_length=150, unique=True, null=True, verbose_name="Имя пользователя")
    full_name = models.CharField(max_length=150, null=True, verbose_name="Ф.И.О")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')

    def __str__(self):
        return self.username if self.username is not None else "Без имени"

    class Meta(AbstractUser.Meta):
        pass

def validate_image(image):
    if image.size > 2 * 1024 * 1024:  # 2 MB
        raise ValidationError('Размер изображения не должен превышать 2 Мб.')
    if not image.name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        raise ValidationError('Неподдерживаемый формат файла. Используйте jpg, jpeg, png или bmp.')

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