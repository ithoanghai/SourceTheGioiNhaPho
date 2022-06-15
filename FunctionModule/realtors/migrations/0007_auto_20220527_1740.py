# Generated by Django 3.1.7 on 2022-05-27 10:40

import FunctionModule.realtors.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('realtors', '0006_auto_20220522_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtor',
            name='phone2',
            field=models.CharField(blank=True, db_index=True, error_messages={'unique': 'Số điện thoại phụ này đã được sử dụng trên hệ thống.'}, max_length=20, validators=[django.core.validators.RegexValidator(message='Số điện thoại 10 số với chỉ các đầu số 09|03|07|08|05', regex='^(09|03|07|08|05)+([0-9]{8})$')], verbose_name='Điện thoại phụ'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='countryside',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Quê quán'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='facebook',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='story',
            field=models.TextField(blank=True, null=True, verbose_name='Kinh nghiệm hoạt động'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='youtube',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Youtube'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='hire_date',
            field=models.DateTimeField(blank=True, default=FunctionModule.realtors.models.default_hire_date, verbose_name='Ngày thêm/gia nhập'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='Họ và tên'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='position',
            field=models.CharField(choices=[('chairperson', 'Chủ tịch'), ('general_manager', 'Tổng giám đốc'), ('manager_director', 'Phó TGĐ/Giám đốc khối'), ('regional_director', 'Giám đốc khu vực/Bá tước'), ('manager', 'Giám đốc chuyên môn/Trưởng phòng'), ('leader', 'Trưởng bộ phận/Trưởng nhóm'), ('assistant', 'Trợ lý'), ('accountant', 'Kế toán'), ('coordinator', 'Điều phối viên'), ('expert_home', 'Chuyên viên Đầu chủ'), ('expert', 'Chuyên viên'), ('interns', 'Học viên')], default='expert', max_length=20, verbose_name='Chức danh'),
        ),

        migrations.AlterField(
            model_name='realtor',
            name='title',
            field=models.CharField(choices=[('superman', 'Siêu nhân'), ('professor', 'Giáo sư'), ('expert', 'Chuyên gia'), ('master', 'Cao thủ'), ('competently', 'Thạo nghề'), ('probationary', 'Tập sự'), ('rookie', 'Tân binh')], default='rookie', max_length=20, verbose_name='Danh hiệu'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL, verbose_name='Tài khoản đăng nhập'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='work_area',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Địa bàn khu vực Quận/Huyện hoạt động'),
        ),
    ]