from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .constants import GENDER_CHOICES


def split_url(url: str) -> str:
    if len(url.split('www.')) >= 2:
        return url.split('www.')[-1]
    elif len(url.split('http://')) >= 2:
        return url.split('http://')[-1]
    elif len(url.split('https://')) >= 2:
        return url.split('https://')[-1]
    else:
        return url


phone_regex = RegexValidator(regex=r'^(09|03|07|08|05)+([0-9]{8})$',
                     message="Số điện thoại 10 số với chỉ các đầu số 09|03|07|08|05")


class User(AbstractUser):
    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "DS Người dùng"
        ordering = ["first_name", "last_name"]

    # These two fields are for backend (admin) login form to display correctly
    username = models.CharField(
        _('Tên đăng nhập'), max_length=150, unique=True,
        help_text=_('Bắt buộc nhập. Không quá 150 ký tự. Có thể bao gồm ký tự, chữ số và chỉ ký tự đặc biệt @/./+/-/_.'),
        error_messages={'unique': _("Người dùng này đã tồn tại trên hệ thống.")},
    )
    email = models.EmailField(_('Email'), blank=True, unique=True, error_messages={
       'unique': _("Email này đã được sử dụng trên hệ thống.")})

    # Basic Info
    first_name = models.CharField(_('Họ'), max_length=150, blank=True)
    last_name = models.CharField(_('Tên'), max_length=150, blank=True)
    phone = models.CharField(_('Điện thoại'), max_length=20, db_index=True, unique=True, validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại này đã được sử dụng trên hệ thống.")})
    address = models.CharField(_('Địa chỉ'), blank=True, max_length=255)
    dob = models.DateField(_('Ngày sinh'), blank=True, null=True)
    gender = models.CharField(_('Giới tính'), max_length=20, choices=GENDER_CHOICES, blank=True, default='male')
    bio = models.TextField(_('Lý lịch'), blank=True)
    avatar = models.ImageField(_("Ảnh đại diện"), upload_to="photos/%Y/%m/%d/", default='img/logo tgnp brown.jpg')

    # Social Fields
    website = models.CharField(_('Website'), blank=True, max_length=255)
    facebook = models.CharField(_('Facebook'), blank=True, max_length=255)
    youtube = models.CharField(_('Youtube'), blank=True, max_length=255)

    # Metadata
    first_time = models.BooleanField(_('Đăng nhập lần đầu'), default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def facebook_url_name(self):
        return split_url(self.facebook)

    @property
    def youtube_url_name(self):
        return split_url(self.youtube)

    @property
    def website_url_name(self):
        return split_url(self.website)

    @property
    def name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username
