# Generated by Django 3.1.7 on 2022-06-09 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0009_auto_20220609_2101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='realtor',
            old_name='identification',
            new_name='identifier',
        ),
    ]