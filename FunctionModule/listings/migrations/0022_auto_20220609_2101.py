# Generated by Django 3.1.7 on 2022-06-09 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0021_auto_20220527_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Giá bán (tỷ), Giá thuê (triệu)'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='road_type',
            field=models.CharField(choices=[('alley_car_2', 'Ô tô tránh'), ('alley_car_tribike', 'Ô tô tránh Ba gác'), ('alley_car', 'Ô tô'), ('alley_tribike', 'Ngõ Ba gác'), ('alley_tribike_bike', 'Ngõ Ba gác tránh Xe máy'), ('alley_bike', 'Ngõ Xe máy tránh nhau')], default='alley_car_tribike', max_length=20, verbose_name='Đường/Ngõ trước nhà'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='transaction_type',
            field=models.CharField(choices=[('sell', 'Bán'), ('rent', 'Cho thuê'), ('project', 'Dự án')], default='sell', max_length=20, verbose_name='Hình thức giao dịch'),
        ),
    ]
