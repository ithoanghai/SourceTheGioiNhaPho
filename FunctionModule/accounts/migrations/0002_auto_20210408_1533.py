# Generated by Django 3.1.7 on 2021-05-10 17:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(db_index=True, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Sai định dạng số điện thoại', regex='^(09|03|07|08|05)+([0-9]{8})$')], verbose_name='Điện thoại'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
    ]