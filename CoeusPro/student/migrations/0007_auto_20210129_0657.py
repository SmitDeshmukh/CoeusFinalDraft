# Generated by Django 3.1.1 on 2021-01-29 06:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20201221_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paperpublications',
            name='year',
            field=models.IntegerField(default=2021, validators=[django.core.validators.MaxValueValidator(9999)], verbose_name='year'),
        ),
    ]
