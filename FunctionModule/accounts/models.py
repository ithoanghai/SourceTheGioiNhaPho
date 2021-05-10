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
                             message="Sai định dạng số điện thoại")


class User(AbstractUser):
    # These two fields are for backend (admin) login form to display correctly

    email = models.EmailField(_('Email'), blank=True)
    is_realtor = models.BooleanField(_("Là đầu chủ"), default=False)
    # Basic Info
    phone = models.CharField(_('Điện thoại'), max_length=20, db_index=True, unique=True,
                             validators=[phone_regex])
    address = models.CharField(_('Địa chỉ'), blank=True, max_length=255)
    dob = models.DateField(_('DoB'), blank=True, null=True)
    gender = models.CharField(_('Gender'), max_length=20, choices=GENDER_CHOICES, blank=True, default='male')
    bio = models.TextField(_('Lý lịch'), blank=True)
    avatar = models.ImageField(_("Ảnh đại diện"), upload_to="photos/%Y/%m/%d/")

    # Social Fields
    website = models.CharField(_('Website'), blank=True, max_length=255)
    facebook = models.CharField(_('Facebook'), blank=True, max_length=255)
    youtube = models.CharField(_('Youtube'), blank=True, max_length=255)

    # Metadata
    first_time = models.BooleanField(_('FirstLogin'), default=True)

    def __str__(self):
        return self.username

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
        return f"{self.first_name} {self.last_name}"
