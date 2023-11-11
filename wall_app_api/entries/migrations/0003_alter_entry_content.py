# Generated by Django 4.2.1 on 2023-11-09 01:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0002_alter_entry_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='content',
            field=models.TextField(validators=[django.core.validators.MaxLengthValidator(limit_value=280, message='Content must be a maximum of 280 characters.')]),
        ),
    ]