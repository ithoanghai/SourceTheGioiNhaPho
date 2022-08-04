# Generated by Django 3.1.7 on 2022-06-09 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0012_auto_20220609_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtor',
            name='status',
            field=models.CharField(choices=[('cooperating', 'Đang hợp tác'), ('pause_cooperating', 'Tạm dừng'), ('stop_cooperating', 'Ngừng hợp tác')], default='cooperating', max_length=20, verbose_name='Hiện trạng'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='position',
            field=models.CharField(choices=[('chairperson', 'Chủ tịch'), ('general_manager', 'Tổng giám đốc'), ('manager_director', 'Phó TGĐ/Giám đốc KD/ GĐ khối'), ('regional_director', 'Giám đốc khu vực/Bá tước'), ('manager', 'Giám đốc chuyên môn/Trưởng phòng'), ('leader', 'Trưởng bộ phận/Trưởng nhóm'), ('assistant', 'Trợ lý'), ('secretary', 'Thư ký'), ('accountant', 'Kế toán'), ('coordinator', 'Điều phối viên'), ('expert_home', 'Chuyên viên Đầu chủ'), ('expert', 'Chuyên viên'), ('interns', 'Học viên')], default='expert', max_length=20, verbose_name='Chức danh'),
        ),
    ]
