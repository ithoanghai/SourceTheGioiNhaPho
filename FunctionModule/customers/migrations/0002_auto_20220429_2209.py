# Generated by Django 3.1.7 on 2022-04-29 15:09

import FunctionModule.customers.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0003_auto_20210815_1839'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='desire',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='potential_points',
        ),
        migrations.AddField(
            model_name='customer',
            name='classify',
            field=models.CharField(choices=[('focused_care', 'Cần chăm tập trung'), ('normal_care', 'Chăm bình thường'), ('slowly_care', 'Chăm từ từ'), ('stop_care', 'Dừng chăm sóc'), ('again_care', 'Chăm sóc lại')], default='focused_care', help_text='Cần chăm tập trung? Chăm bình thường? Chăm từ từ?', max_length=50, verbose_name='Kết luận chăm khách'),
        ),
        migrations.AddField(
            model_name='customer',
            name='contact_from',
            field=models.CharField(blank=True, help_text='Khách tìm từ nguồn nào (Face, website, giới thiệu)? Liên hệ từ căn nào? BĐS thật hay chim mồi?...', max_length=500, null=True, verbose_name='Liên hệ từ đâu'),
        ),
        migrations.AddField(
            model_name='customer',
            name='custormer_type',
            field=models.CharField(choices=[('buy_to_live', 'Mua ở'), ('keep_money', 'Giữ tiền'), ('invest_construction', 'Đầu tư xây bán'), ('surf_investment', 'Đầu tư lướt sóng')], default='buy_to_live', max_length=20, verbose_name='Loại khách'),
        ),
        migrations.AddField(
            model_name='customer',
            name='descriptions',
            field=models.TextField(blank=True, help_text='Nơi ở, nơi làm việc, nghề nghiệp, tình trạng hôn nhân,...Mục đích mua nhà (Để ở, đầu tư, để kinh doanh, vừa ở vừa kinh doanh). Khu vực nào? Vị trí mong muốn (gần đường, ngõ rộng,...)?. Có nhu cầu về ô tô hay không?,Khách có yêu cầu đi xem luôn hay không?,...', null=True, verbose_name='Thông tin nhu cầu cơ bản'),
        ),
        migrations.AddField(
            model_name='customer',
            name='district',
            field=models.CharField(blank=True, help_text='Khu vực khách quan tâm. Dùng dấu phảy (,) để ngăn cách', max_length=500, null=True, verbose_name='Khu vực quan tâm'),
        ),
        migrations.AddField(
            model_name='customer',
            name='financial_range',
            field=models.DecimalField(decimal_places=2, help_text='Tài chính khách thu xếp được', max_digits=5, null=True, verbose_name='Tầm tài chính (tỷ)'),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_interaction',
            field=models.DateField(blank=True, default=FunctionModule.customers.models.default_hire_date, verbose_name='Thời điểm tương tác gần nhất'),
        ),
        migrations.AddField(
            model_name='customer',
            name='listing_watched',
            field=models.TextField(blank=True, help_text='Địa chỉ nhà đã xem? Ai dẫn xem? Thời gian xem? Ý kiến về BĐS này?,...', null=True, verbose_name='BĐS đã xem và phản hồi của khách'),
        ),
        migrations.AddField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=150, null=True, verbose_name='Tên khách hàng'),
        ),
        migrations.AddField(
            model_name='customer',
            name='request',
            field=models.TextField(blank=True, help_text='Mục đích mua nhà (Để ở, đầu tư, để kinh doanh, vừa ở vừa kinh doanh). Khu vực nào? Vị trí mong muốn (gần đường, ngõ rộng,...)?. Có nhu cầu về ô tô hay không?,...', null=True, verbose_name='Nhu cầu'),
        ),
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('new', 'Mới đi xem nhà'), ('see_more', 'Xem đã nhiều nhưng chưa ưng BĐS nào'), ('missed_purchase', 'Đã từng chốt hụt')], default='see_more', help_text='Mới đi xem nhà. Cần mua gấp. Xem đã nhiều nhưng chưa ưng BĐS nào? Chốt hụt căn nào không?', max_length=50, verbose_name='Tình trạng chốt'),
        ),
        migrations.AddField(
            model_name='customer',
            name='transactionStatus',
            field=models.CharField(choices=[('need', 'Cần mua gấp'), ('not_yet', 'Chưa mua'), ('pause_buying', 'Tạm dừng mua'), ('bought', 'Đã mua'), ('stop_buying', 'Dừng quan tâm')], default='not_yet', max_length=50, verbose_name='Mức độ giao dịch'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Địa chỉ thường trú'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, error_messages={'unique': 'Email này đã được sử dụng trên hệ thống.'}, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='hire_date',
            field=models.DateField(blank=True, default=FunctionModule.customers.models.default_hire_date, verbose_name='Thời điểm thêm'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(db_index=True, error_messages={'unique': 'Số điện thoại này đã được người khác sử dụng trên hệ thống.'}, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Số điện thoại 10 số với chỉ các đầu số 09|03|07|08|05', regex='^(09|03|07|08|05)+([0-9]{8})$')], verbose_name='Điện thoại'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='realtor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='realtors.realtor', verbose_name='Giao Chuyên viên chăm sóc'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Người thêm KH'),
        ),
    ]
