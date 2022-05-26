# Generated by Django 3.1.7 on 2022-05-24 15:57

import FunctionModule.realtors.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realtors', '0006_auto_20220522_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realtor',
            name='user',
        ),
        migrations.AddField(
            model_name='realtor',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='Nơi ở hiện tại'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='birthyear',
            field=models.IntegerField(choices=[(1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006)], default=2007, verbose_name='Năm sinh'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='countryside',
            field=models.CharField(blank=True, max_length=150, verbose_name='Quê quán'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Bộ phận/Phòng/Ban'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='email',
            field=models.EmailField(blank=True, error_messages={'unique': 'Email này đã được sử dụng trên hệ thống.'}, max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='facebook',
            field=models.CharField(blank=True, max_length=255, verbose_name='Facebook'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='is_cooperate',
            field=models.BooleanField(default=False, verbose_name='ĐANG HỢP TÁC VỚI TGNP'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='CÔNG KHAI DANH TÍNH'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='phone1',
            field=models.CharField(blank=True, db_index=True, error_messages={'unique': 'Số điện thoại chính này đã được sử dụng trên hệ thống.'}, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Số điện thoại 10 số với chỉ các đầu số 09|03|07|08|05', regex='^(09|03|07|08|05)+([0-9]{8})$')], verbose_name='Điện thoại chính'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='phone2',
            field=models.CharField(blank=True, db_index=True, error_messages={'unique': 'Số điện thoại phụ này đã được sử dụng trên hệ thống.'}, max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Số điện thoại 10 số với chỉ các đầu số 09|03|07|08|05', regex='^(09|03|07|08|05)+([0-9]{8})$')], verbose_name='Điện thoại phụ'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='story',
            field=models.TextField(blank=True, verbose_name='Tiểu sử hoạt động'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='website',
            field=models.CharField(blank=True, max_length=255, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='workplace',
            field=models.CharField(choices=[('tgnp', 'Thế Giới Nhà Phố'), ('thienkhoi', 'Thiên Khôi'), ('nhapho', 'Nhà Phố VN'), ('kimland', 'Kim Land'), ('tuan123', 'Tuấn 123'), ('phoxanh', 'Phố Xanh'), ('sumo', 'Sumo'), ('vuda', 'Vuda Home'), ('other', 'Đơn vị khác')], default='tgnp', max_length=50, verbose_name='Đơn vị'),
        ),
        migrations.AddField(
            model_name='realtor',
            name='youtube',
            field=models.CharField(blank=True, max_length=255, verbose_name='Youtube'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='hire_date',
            field=models.DateTimeField(blank=True, default=FunctionModule.realtors.models.default_hire_date, verbose_name='Ngày thêm/gia nhập'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Họ tên'),
        ),
        migrations.AlterField(
            model_name='realtor',
            name='position',
            field=models.CharField(choices=[('chairperson', 'Chủ tịch'), ('general_manager', 'Tổng giám đốc'), ('manager_director', 'Phó TGĐ/Giám đốc khối'), ('regional_director', 'Giám đốc khu vực/Bá tước'), ('manager', 'Giám đốc chuyên môn/Trưởng phòng'), ('leader', 'Trưởng bộ phận/Trưởng nhóm'), ('assistant', 'Trợ lý'), ('accountant', 'Kế toán'), ('coordinator', 'Điều phối viên'), ('expert_home', 'Chuyên viên Đầu chủ'), ('expert', 'Chuyên viên'), ('interns', 'Học viên')], default='expert', max_length=20, verbose_name='Chức danh'),
        ),
    ]
