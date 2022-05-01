# Generated by Django 3.1.7 on 2021-09-04 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_merge_20210904_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionhistory',
            name='status',
            field=models.CharField(choices=[('active', 'Đang giao dịch'), ('pause', 'Tạm dừng'), ('cancelTransaction', 'Huỷ'), ('completed', 'Hoàn thành')], default='active', max_length=25, verbose_name='Trạng thái giao dịch'),
        ),
    ]