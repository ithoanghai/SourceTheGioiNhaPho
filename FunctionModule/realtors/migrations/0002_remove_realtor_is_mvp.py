# Generated by Django 3.1.7 on 2021-07-11 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realtor',
            name='is_mvp',
        ),
    ]
