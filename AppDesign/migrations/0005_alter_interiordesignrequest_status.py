# Generated by Django 3.2.25 on 2024-12-09 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppDesign', '0004_auto_20241209_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interiordesignrequest',
            name='status',
            field=models.CharField(choices=[('Новая', 'Новая'), ('В процессе', 'В процессе'), ('Завершена', 'Завершена')], default='Новая', max_length=20, verbose_name='Статус'),
        ),
    ]
