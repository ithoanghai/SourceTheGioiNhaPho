from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from FunctionModule.accounts.models import User, phone_regex
from FunctionModule.customers.choices import CustomerStatus, CustomerClassify, TransactionStatus, CustomerType
from FunctionModule.listings.choices import district_choices, city_choices
from FunctionModule.realtors.models import Realtor


def default_hire_date():
    return timezone.now()


class Customer(models.Model):
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "DS Khách hàng"

    indexes = (
        # Exact search
        models.Index(fields=["district"]),
    )

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.RESTRICT, verbose_name=_("Người thêm KH"))
    realtor = models.ForeignKey(Realtor, null=True, blank=True, on_delete=models.RESTRICT, verbose_name=_("Giao Chuyên viên chăm sóc"))
    custormer_type = models.CharField(max_length=20, choices=CustomerType.choices, default=CustomerType.BUY_LIVE,
                                 verbose_name=_("Loại khách"))
    name = models.CharField(_('Tên khách hàng'), null=True, max_length=150)
    phone = models.CharField(_('Điện thoại'), max_length=20, db_index=True, unique=True, validators=[phone_regex],
                             error_messages={'unique': _("Số điện thoại này đã được người khác sử dụng trên hệ thống.")})
    email = models.EmailField(_('Email'), null=True, blank=True, error_messages={
        'unique': _("Email này đã được sử dụng trên hệ thống.")})
    address = models.CharField(_('Địa chỉ thường trú'), null=True, blank=True, max_length=255)
    financial_range = models.DecimalField(max_digits=5, decimal_places=2, null=True, verbose_name=_("Tầm tài chính (tỷ)"), help_text=_("Tài chính khách thu xếp được"))
    district = models.CharField(max_length=500, null=True, blank=True, verbose_name=_("Khu vực quan tâm"), help_text=_("Khu vực khách quan tâm. Dùng dấu phảy (,) để ngăn cách"))
    descriptions = models.TextField(_('Thông tin, Nhu cầu cơ bản'), null=True, blank=True, help_text=_(
        "Nơi ở, nơi làm việc, nghề nghiệp, tình trạng hôn nhân,...Mục đích mua nhà (Để ở, đầu tư, để kinh doanh, vừa ở vừa kinh doanh). Khu vực nào? Vị trí mong muốn (gần đường, ngõ rộng,...)?. Có nhu cầu về ô tô hay không?,Khách có yêu cầu đi xem luôn hay không?,..."))
    contact_from = models.CharField(_('Liên hệ từ đâu'), max_length=500, null=True, blank=True, help_text=_(
        "Khách tìm từ nguồn nào (Face, website, ai giới thiệu)? Liên hệ từ căn nào? BĐS thật hay chim mồi?..."))
    listing_watched = models.TextField(_('BĐS đã xem và phản hồi của khách'), null=True, blank=True, help_text=_(
        "Địa chỉ nhà đã xem? Ai dẫn xem? Thời gian xem? Ý kiến về BĐS này?,..."))
    status = models.CharField(max_length=50, choices=CustomerStatus.choices, default=CustomerStatus.SEE_MORE, verbose_name=_("Tình trạng chốt"),
                                help_text=_("Mới đi xem nhà. Cần mua gấp. Xem đã nhiều nhưng chưa ưng BĐS nào? Chốt hụt căn nào không?"))
    transactionStatus = models.CharField(max_length=50, choices=TransactionStatus.choices, default=TransactionStatus.NOT_YET, verbose_name=_("Trạng thái giao dịch"),)
    classify = models.CharField(max_length=50, choices=CustomerClassify.choices, default=CustomerClassify.FOCUSED_CARE, verbose_name=_("Kết luận chăm khách"),
                              help_text=_("Cần chăm tập trung? Chăm bình thường? Chăm từ từ?"))
    #potential_points = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True, default='0', verbose_name=_("Điểm tiềm năng"))
    hire_date = models.DateField(verbose_name=_("Thời điểm thêm"), default=default_hire_date, blank=True)
    last_interaction = models.DateField(verbose_name=_("Thời điểm tương tác gần nhất"), default=default_hire_date, blank=True)

    def __str__(self):
        return str(self.name)


