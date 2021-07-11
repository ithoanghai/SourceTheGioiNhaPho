# Generated by Django 3.1.7 on 2021-06-25 14:23

import django.contrib.gis.geos.point
from django.db import migrations, models
import embed_video.fields
import location_field.models.spatial


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_auto_20210622_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='furniture_design',
            field=models.TextField(blank=True, help_text='Thiết kế hiện đại, đầy đủ công năng, khung cột bê tông chắc chắn hay không, Có hay không có nội thất kèm theo, kèm theo những nội thất', null=True, verbose_name='Nội thất, thiết kế'),
        ),
        migrations.AddField(
            model_name='listing',
            name='living_facilities',
            field=models.TextField(blank=True, help_text='Có bể bơi, phòng xông hơi, xem phim, thể thao, có chỗ đỗ xe hơi,...', null=True, verbose_name='Tiện ích sinh hoạt'),
        ),
        migrations.AddField(
            model_name='listing',
            name='location_advantage',
            field=models.TextField(blank=True, help_text='Mô tả ưu điểm của vị trí, gần địa điểm nổi tiếng, dễ nhớ nào, khoảng bao nhiêu phút ra trung tâm, đường chính, hồ, bến tàu, xe, sân vận động, rạp chiếu phim..', null=True, verbose_name='Ưu điểm vị trí'),
        ),
        migrations.AddField(
            model_name='listing',
            name='regional_welfare',
            field=models.TextField(blank=True, help_text='Gần trường mầm non, tiểu học, THCS,...Bệnh viện, Trung tâm spa, chăm sóc sức khoẻ, sắc đẹp...', null=True, verbose_name='An sinh khu vực'),
        ),
        migrations.AddField(
            model_name='listing',
            name='residential_community',
            field=models.TextField(blank=True, help_text='Cộng đồng dân cư dân trí cao, văn minh, an ninh, thân thiện hay không', null=True, verbose_name='Cộng đồng dân cư'),
        ),
        migrations.AddField(
            model_name='listing',
            name='salient_features',
            field=models.TextField(blank=True, help_text='Nêu tất cả các ưu điểm nổi bật của BĐS', null=True, verbose_name='Đặc điểm nổi bật'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='address',
            field=models.CharField(help_text='Ngõ.Ngách.Hẻm.Số nhà, Khu dân cư, Phố, Quận/Huyện, Tỉnh/TP', max_length=255, verbose_name='Địa chỉ đầy đủ'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.TextField(blank=True, help_text='Mô tả giới thiệu BĐS ngắn gọn ', verbose_name='Mô tả ngắn gọn'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='location',
            field=location_field.models.spatial.LocationField(default=django.contrib.gis.geos.point.Point(105.8401439, 21.0334474), help_text='Nhập toạ độ hoặc chọn vị trí trên bản đồ', null=True, srid=4326, verbose_name='Toạ độ vị trí BĐS'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='reward_person_mobile',
            field=models.CharField(blank=True, default='0916286256', help_text='Số ĐT chủ sở hữu BĐS', max_length=50, verbose_name='Số ĐT chủ sở hữu BĐS'),
        ),
        migrations.AlterField(
            model_name='listingvideo',
            name='video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
