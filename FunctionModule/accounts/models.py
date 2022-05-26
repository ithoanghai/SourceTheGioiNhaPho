from datetime import datetime

from django.contrib.auth.models import AbstractUser, Permission, GroupManager, UserManager
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .constants import GENDER_CHOICES


def default_hire_date():
    return timezone.now()


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
        help_text=_(
            'Bắt buộc nhập. Không quá 150 ký tự. Có thể bao gồm ký tự, chữ số và chỉ ký tự đặc biệt @/./+/-/_.'),
        error_messages={'unique': _("Người dùng này đã tồn tại trên hệ thống.")},
    )
    email = models.EmailField(_('Email'), blank=True, unique=True, error_messages={
        'unique': _("Email này đã được sử dụng trên hệ thống.")})

    # Basic Info
    first_name = models.CharField(_('Họ Đệm'), max_length=150, blank=True)
    last_name = models.CharField(_('Tên'), max_length=150, blank=True)
    phone = models.CharField(_('Điện thoại'), max_length=20, db_index=True, unique=True,
                             validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại này đã được sử dụng trên hệ thống.")})
    address = models.CharField(_('Địa chỉ nơi ở'), blank=True, max_length=255)
    dob = models.DateField(_('Ngày sinh'), blank=True, null=True)
    gender = models.CharField(_('Giới tính'), max_length=20, choices=GENDER_CHOICES, blank=True,
                              default='male')
    bio = models.TextField(_('Giới thiệu bản thân'), blank=True)
    avatar = models.ImageField(_("Ảnh đại diện"), upload_to="photos/%Y%m%d/", blank=True)

    is_broker = models.BooleanField(default=False, verbose_name=_("MUỐN LÀM MÔI GIỚI"))
    is_investor = models.BooleanField(default=False, verbose_name=_("MUỐN LÀM ĐẦU TƯ"))
    is_active = models.BooleanField(default=True, verbose_name=_("ĐÃ KÍCH HOẠT"))
    is_staff = models.BooleanField(default=False, verbose_name=_("LÀ CHUYÊN VIÊN TGNP"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("LÀ QUẢN TRỊ HỆ THỐNG"))
    # Metadata
    first_time = models.BooleanField(_('Đăng nhập lần đầu'), default=True)
    date_joined = models.DateField(_('Ngày gia nhập'), default=timezone.now, blank=True, null=True)

    objects = UserManager()

    def __str__(self):
        return f'%s - %s' % (self.name, self.phone)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    @property
    def name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    def user_image(self):
        return '<img src="%s"/>' % self.avatar

    user_image.allow_tags = True


class Group(models.Model):
    """
    Overwrites original Django Group.
    """
    class Meta:
        verbose_name = "Nhóm người dùng"
        verbose_name_plural = "DS Nhóm người dùng"

    name = models.CharField(_('Tên nhóm'), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        to='auth.Permission',
        verbose_name=_('Quyền sử dụng'),
        blank=True,
        related_name='permissions2permissions'
    )

    objects = GroupManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Point(models.Model):
    class Meta:
        verbose_name = "Điểm số"
        verbose_name_plural = "Điểm đạt được"

    user = models.OneToOneField(User, on_delete=models.RESTRICT, db_constraint=User, blank=True, null=True)
    investment_point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm đầu tư"), null=True, blank=True, default=0)
    investment_account = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999999)],
                                           verbose_name=_("Tài khoản có đầu tư (Triệu đồng)"), null=True, blank=True, default=0)
    prestige_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm uy tín"), null=True, blank=True, default=0)
    potential_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm tiềm năng"), null=True, blank=True, default=0)
    bds_referral_point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm giới thiệu BĐS"), null=True, blank=True,default=0)
    customer_referral_point = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], verbose_name=_("Điểm giới thiệu khách"), null=True, blank=True,default=0)

    def __str__(self):
        return f'%s' % (self.user)