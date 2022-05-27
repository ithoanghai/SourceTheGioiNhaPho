from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from FunctionModule.accounts.models import User
from FunctionModule.listings.choices import Position, Title, Workplace


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
        verbose_name = "Chuyên viên"
        verbose_name_plural = "DS Chuyên viên"

    user = models.OneToOneField(User, on_delete=models.RESTRICT, verbose_name=_("Tài khoản đăng nhập"), blank=True, null=True)
    name = models.CharField(max_length=50, null=True, verbose_name=_("Họ và tên"))
    position = models.CharField(max_length=20, choices=Position.choices, verbose_name=_("Chức danh"),default=Position.EXPERT)
    birthyear = models.IntegerField(_('Năm sinh'), blank=True, null=True, choices=year_dropdown, default=timezone.now().year - 15)
    countryside = models.CharField(_('Quê quán'), blank=True, max_length=150)
    phone1 = models.CharField(_('Điện thoại chính'), max_length=20, db_index=True, unique=True, validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại chính này đã được sử dụng trên hệ thống.")})
    phone2 = models.CharField(_('Điện thoại phụ'), max_length=20, db_index=True, blank=True, null=True, validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại phụ này đã được sử dụng trên hệ thống.")})
    email = models.EmailField(_('Email'), blank=True, null=True)
    address = models.CharField(_('Nơi ở hiện tại'), blank=True, max_length=255)
    title = models.CharField(max_length=20, choices=Title.choices, verbose_name=_("Danh hiệu"), default=Title.ROOKIE)
    level = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)], choices=([(i, i) for i in range(1, 10)]), default=1, verbose_name=_("Đẳng cấp chuyên môn"))
    workplace = models.CharField(max_length=50, choices=Workplace.choices, verbose_name=_("Đơn vị"), default=Workplace.TGNP)
    department = models.CharField(max_length=100, verbose_name=_("Bộ phận/Phòng/Ban"), null=True, blank=True)
    work_area = models.CharField(max_length=100, verbose_name=_("Địa bàn khu vực Quận/Huyện hoạt động"), null=True, blank=True)
    story = models.TextField(_('Kinh nghiệm hoạt động'), blank=True)
    # Social Fields
    website = models.CharField(_('Website'), blank=True, max_length=255)
    facebook = models.CharField(_('Facebook'), null=True, max_length=255)
    youtube = models.CharField(_('Youtube'), blank=True, max_length=255)

    hire_date = models.DateTimeField(default=default_hire_date, verbose_name=_("Ngày thêm/gia nhập"), blank=True)
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
