# Generated by Django 3.1.7 on 2021-06-22 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(blank=True, null=True, verbose_name='Ngày sinh'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_time',
            field=models.BooleanField(default=True, verbose_name='Đăng nhập lần đầu'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Nam'), ('female', 'Nữ')], default='male', max_length=20, verbose_name='Giới tính'),
        ),
    ]