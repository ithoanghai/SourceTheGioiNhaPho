# Generated by Django 3.1.6 on 2021-03-27 04:01

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('is_realtor', models.BooleanField(default=False, verbose_name='Là đầu chủ')),
                ('phone', models.CharField(db_index=True, max_length=20, verbose_name='Điện thoại', unique=True)),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Địa chỉ')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='DoB')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Nam'), ('female', 'Nữ')], default='male', max_length=20, verbose_name='Gender')),
                ('bio', models.TextField(blank=True, verbose_name='Lý lịch')),
                ('avatar', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Ảnh đại diện')),
                ('website', models.CharField(blank=True, max_length=255, verbose_name='Website')),
                ('facebook', models.CharField(blank=True, max_length=255, verbose_name='Facebook')),
                ('youtube', models.CharField(blank=True, max_length=255, verbose_name='Youtube')),
                ('first_time', models.BooleanField(default=True, verbose_name='FirstLogin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
