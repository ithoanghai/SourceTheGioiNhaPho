# Generated by Django 3.1.14 on 2022-09-05 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0030_auto_20220904_0105'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='full_path',
            field=models.TextField(blank=True, null=True),
        ),
    ]