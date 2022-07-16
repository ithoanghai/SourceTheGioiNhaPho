from datetime import datetime

from django.contrib.auth.models import AbstractUser, GroupManager, UserManager, PermissionManager, \
    _user_has_module_perms, _user_get_permissions, _user_has_perm
from django.contrib.contenttypes.models import ContentType
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


class Permission(models.Model):
    """
    The permissions system provides a way to assign permissions to specific
    users and groups of users.

    The permission system is used by the Django admin site, but may also be
    useful in your own code. The Django admin site uses permissions as follows:

        - The "add" permission limits the user's ability to view the "add" form
          and add an object.
        - The "change" permission limits a user's ability to view the change
          list, view the "change" form and change an object.
        - The "delete" permission limits the ability to delete an object.
        - The "view" permission limits the ability to view an object.

    Permissions are set globally per type of object, not per specific object
    instance. It is possible to say "Mary may change news stories," but it's
    not currently possible to say "Mary may change news stories, but only the
    ones she created herself" or "Mary may only change news stories that have a
    certain status or publication date."

    The permissions listed above are automatically created for each model.
    """
    name = models.CharField(_('Tên quyền'), max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name=_('Chức năng'),
        related_name='django'
    )
    codename = models.CharField(_('Mã chức năng'), max_length=100)

    objects = PermissionManager()

    class Meta:
        verbose_name = _('Quyền sử dụng')
        verbose_name_plural = _('DS Quyền sử dụng')
        unique_together = [['content_type', 'codename']]
        ordering = ['content_type__app_label', 'content_type__model', 'codename']

    def __str__(self):
        return '%s | %s' % (self.content_type, self.name)

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']


class CustomGroup(models.Model):
    """
    Overwrites original Django Group.
    """
    class Meta:
        verbose_name = "Nhóm người dùng"
        verbose_name_plural = "DS Nhóm người dùng"

    name = models.CharField(_('Tên nhóm'), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        to='accounts.Permission',
        verbose_name=_('Quyền sử dụng'),
        blank=True,
        related_name='customgroup'
    )

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class PermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    customgroup = models.ManyToManyField(
        CustomGroup,
        verbose_name=_('Nhóm người dùng'),
        blank=True,
        help_text=_(
            'Nhóm quyền mà người dùng này được phân quyền.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('Quyền người dùng'),
        blank=True,
        help_text=_('Xác định quyền cho người dùng này.'),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True


class User(AbstractUser, PermissionsMixin):
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
    last_login = models.DateTimeField(_('Đăng nhập lần cuối'), default=timezone.now, blank=True, null=True)

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