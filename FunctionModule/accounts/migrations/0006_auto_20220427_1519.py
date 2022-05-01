# Generated by Django 3.1.7 on 2022-04-27 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0005_auto_20220104_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='photos/%Y%m%d/', verbose_name='Ảnh đại diện'),
        ),
        migrations.CreateModel(
            name='CustomGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_alias', models.EmailField(blank=True, default='', max_length=70)),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='auth.group')),
            ],
            options={
                'verbose_name': 'Nhóm người dùng',
                'verbose_name_plural': 'DS Nhóm người dùng',
            },
        ),
    ]