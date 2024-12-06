import re
from django.core.exceptions import ValidationError

def validate_cyrillic(value):
    if not re.match(r'^[А-Яа-яЁё\s-]+$', value):
        raise ValidationError('Поле должно содержать только кириллические символы, пробелы и дефисы.')