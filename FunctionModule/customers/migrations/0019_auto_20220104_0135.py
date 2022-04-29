# Generated by Django 3.1.7 on 2022-01-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0018_auto_20211214_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='custormer_type',
            field=models.CharField(choices=[('buy_to_live', 'Mua ở'), ('keep_money', 'Giữ tiền'), ('invest_construction', 'Đầu tư xây bán'), ('surf_investment', 'Đầu tư lướt sóng')], default='buy_to_live', max_length=20, verbose_name='Loại khách'),
        ),
        migrations.AddField(
            model_name='customer',
            name='transactionStatus',
            field=models.CharField(choices=[('need', 'Cần mua gấp'), ('not_yet', 'Chưa mua'), ('pause_buying', 'Tạm dừng mua'), ('bought', 'Đã mua'), ('stop_buying', 'Dừng quan tâm')], default='not_yet', max_length=50, verbose_name='Mức độ giao dịch'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='classify',
            field=models.CharField(choices=[('focused_care', 'Cần chăm tập trung'), ('normal_care', 'Chăm bình thường'), ('slowly_care', 'Chăm từ từ'), ('stop_care', 'Dừng chăm sóc'), ('again_care', 'Chăm sóc lại'), ('bought', 'Đã mua nhà rồi')], default='focused_care', help_text='Cần chăm tập trung? Chăm bình thường? Chăm từ từ?', max_length=50, verbose_name='Mức độ chăm khách'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('new', 'Mới đi xem nhà'), ('see_more', 'Xem đã nhiều nhưng chưa ưng BĐS nào'), ('missed_purchase', 'Đã từng chốt hụt')], default='see_more', help_text='Mới đi xem nhà. Cần mua gấp. Xem đã nhiều nhưng chưa ưng BĐS nào? Chốt hụt căn nào không?', max_length=50, verbose_name='Tình trạng chốt'),
        ),
    ]
