# Generated by Django 3.1.14 on 2022-08-04 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_auto_20220513_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='classify',
            field=models.CharField(choices=[('focused_care', 'Khách nét. Cần chăm tập trung'), ('normal_care', 'Chăm bình thường'), ('slowly_care', 'Chăm từ từ'), ('stop_care', 'Dừng chăm sóc'), ('again_care', 'Chăm sóc lại')], default='focused_care', help_text='Cần chăm tập trung? Chăm bình thường? Chăm từ từ?', max_length=50, verbose_name='Kết luận chăm khách'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_from',
            field=models.CharField(blank=True, help_text='Khách tìm từ nguồn nào (Face, website, ai giới thiệu)? Liên hệ từ căn nào? BĐS thật hay chim mồi?...', max_length=500, null=True, verbose_name='Liên hệ từ đâu'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='descriptions',
            field=models.TextField(blank=True, help_text='Nơi ở, nơi làm việc, nghề nghiệp, tình trạng hôn nhân,...Mục đích mua nhà (Để ở, đầu tư, để kinh doanh, vừa ở vừa kinh doanh). Khu vực nào? Vị trí mong muốn (gần đường, ngõ rộng,...)?. Có nhu cầu về ô tô hay không?,Khách có yêu cầu đi xem luôn hay không?,...', null=True, verbose_name='Nhu cầu cơ bản'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='transactionStatus',
            field=models.CharField(choices=[('need', 'Cần mua gấp'), ('not_yet', 'Chưa mua'), ('pause_buying', 'Tạm dừng mua'), ('bought', 'Đã mua'), ('stop_buying', 'Dừng quan tâm')], default='not_yet', max_length=50, verbose_name='Trạng thái giao dịch'),
        ),
    ]
