import sys
from io import BytesIO
import os.path

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import pre_delete, post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from FunctionModule.accounts.models import User
from FunctionModule.realtors.choices import Position, Title, Workplace, Status
from TownhouseWorldRealestate.settings import AVATAR_PHOTO_URL


def split_url(url: str) -> str:
    if len(url.split('www.')) >= 2:
        return url.split('www.')[-1]
    elif len(url.split('http://')) >= 2:
        return url.split('http://')[-1]
    elif len(url.split('https://')) >= 2:
        return url.split('https://')[-1]
    else:
        return url


def default_hire_date():
    return timezone.now()


phone_regex = RegexValidator(regex=r'^(09|03|07|08|05)+([0-9]{8})$',
                             message="Số điện thoại 10 số với chỉ các đầu số 09|03|07|08|05")

year_dropdown = []
for y in range(1950, (timezone.now().year - 15)):
    year_dropdown.append((y, y))


class Realtor(models.Model):
    class Meta:
        verbose_name = _("Chuyên viên")
        verbose_name_plural = _("Chuyên viên")

    user = models.OneToOneField(to=User, on_delete=models.RESTRICT, verbose_name=_("Tài khoản đăng nhập của chuyên viên"), blank=True, null=True)
    name = models.CharField(max_length=50,  null=True,  verbose_name=_("Họ và tên"))
    position = models.CharField(max_length=20, choices=Position.choices, verbose_name=_("Chức danh"),default=Position.EXPERT)
    birthyear = models.IntegerField(verbose_name=_('Năm sinh'), blank=True, null=True, choices=year_dropdown)
    countryside = models.CharField(verbose_name=_('Quê quán'), blank=True, null=True, max_length=150)
    phone1 = models.CharField(verbose_name=_('Điện thoại chính'), max_length=40, null=True, db_index=True, unique=True, validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại chính này đã được sử dụng trên hệ thống.")})
    phone2 = models.CharField(verbose_name=_('Điện thoại phụ'), max_length=40, db_index=True, blank=True, null=True, validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại phụ này đã được sử dụng trên hệ thống.")})
    avatar = models.ImageField(verbose_name=_("Ảnh đại diện"), upload_to=AVATAR_PHOTO_URL, blank=True)

    identifier = models.CharField(verbose_name=_('Căn cước công dân'), blank=True, null=True, max_length=25)
    workplace = models.CharField(max_length=50, choices=Workplace.choices, verbose_name=_("Đơn vị"),
                                 default=Workplace.TGNP)
    department = models.CharField(max_length=100, verbose_name=_("Bộ phận/Phòng/Ban"), null=True, blank=True)
    email = models.EmailField(verbose_name=_('Email'), blank=True, null=True)
    address = models.CharField(verbose_name=_('Nơi ở hiện tại'), blank=True, null=True, max_length=255)
    title = models.CharField(max_length=30, choices=Title.choices, verbose_name=_("Danh hiệu"), default=Title.ROOKIE)
    level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], choices=([(i, i) for i in range(1, 10)]), default=1, verbose_name=_("Đẳng cấp chuyên môn"))
    work_area = models.CharField(max_length=100, verbose_name=_("Địa bàn khu vực Quận/Huyện hoạt động"), null=True, blank=True)
    story = models.TextField(verbose_name=_('Kinh nghiệm hoạt động'), blank=True, null=True,)
    # Social Fields
    website = models.CharField(verbose_name=_('Website'), blank=True, null=True, max_length=255)
    facebook = models.CharField(verbose_name=_('Facebook'), blank=True, null=True, max_length=255)
    youtube = models.CharField(verbose_name=_('Youtube'), blank=True, null=True, max_length=255)
    training = models.CharField(verbose_name=_('Khóa đào tạo'), blank=True, null=True, max_length=50)
    referral = models.CharField(verbose_name=_('Nguồn tuyển'), blank=True, null=True, max_length=100)

    date_join = models.DateField(default=default_hire_date, verbose_name=_("Ngày vào đơn vị"), blank=True, null=True,)
    hire_date = models.DateField(default=default_hire_date, verbose_name=_("Ngày thêm chuyên viên"), blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, verbose_name=_("Hợp tác với đơn vị cũ"), default=Status.COOPERATING)
    is_cooperate = models.BooleanField(default=False, verbose_name=_("ĐANG HỢP TÁC VỚI TGNP"))
    is_published = models.BooleanField(default=False, verbose_name=_("CÔNG KHAI DANH TÍNH"))

    def __str__(self):
        return f'%s - %s' % (self.name, self.phone1)

    @property
    def facebook_url_name(self):
        return split_url(self.facebook)

    @property
    def youtube_url_name(self):
        return split_url(self.youtube)

    @property
    def website_url_name(self):
        return split_url(self.website)

    def birth(self):
        if self.birthyear:
            return f"{self.birthyear}"

    def user_image(self):
        return '<img src="%s"/>' % self.avatar

    user_image.allow_tags = True

    def join_date(self):
        if self.date_join:
            return self.date_join.strftime('%d/%m/%Y')
        return ''

    @receiver(post_delete, sender=Image)
    def post_save_image(sender, instance, *args, **kwargs):
        """ Clean Old Image file """
        try:
            instance.avatar.delete(save=False)
        except:
            pass

    @receiver(pre_save, sender=Image)
    def pre_save_image(sender, instance, *args, **kwargs):
        """ instance old image file will delete from os """
        try:
            old_img = instance.__class__.objects.get(id=instance.id).avatar.path
            try:
                new_img = instance.image.path
            except:
                new_img = None
            if new_img != old_img:
                import os
                if os.path.exists(old_img):
                    os.remove(old_img)
        except:
            pass

    def save(self, *args, **kwargs):
        #self.remove_on_image_update()
        # is the object in the database yet?
        if self.id:
            obj = get_object_or_404(Realtor, pk=self.id)
            # is the save due to an update of the actual image file?
            if obj.avatar and self.avatar and obj.avatar != self.avatar:
                # delete the old image file from the storage in favor of the new file
                obj.avatar.delete(save=True)

                # Opening the uploaded image
                im = Image.open(self.avatar)
                output = BytesIO()

                if im.width > 400 or im.height > 600:
                    # Resize/modify the image
                    output_size = (400, 600)
                    im.thumbnail(output_size)

                # after modifications, save it to the output
                im.save(output, format='JPEG', quality=90)
                output.seek(0)

                # change the imagefield value to be the newley modifed image value
                self.avatar = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.avatar.name.split('.')[0], 'image/jpeg',
                                                  sys.getsizeof(output), None)

        return super(Realtor, self).save(*args, **kwargs)


class RealtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realtor
        exclude = ()

    name = serializers.CharField()
    phone1 = serializers.CharField()
    identifier = serializers.CharField()
    birthyear = serializers.IntegerField()
    date_join = serializers.DateField()
    position = serializers.FloatField()
    workplace = serializers.FloatField()
    department = serializers.CharField()
    facebook = serializers.CharField()
    email = serializers.CharField()
    address = serializers.CharField()
    countryside = serializers.CharField()
    work_area = serializers.CharField()
    status = serializers.CharField()
    is_cooperate = serializers.BooleanField()
    is_published = serializers.BooleanField()
    training = serializers.CharField()
    referral = serializers.CharField()
    hire_date = serializers.DateField()
